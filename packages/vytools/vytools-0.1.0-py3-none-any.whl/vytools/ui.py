import os, json, sys, threading
from pathlib import Path
from vytools.config import CONFIG, ITEMS
import vytools.utils as utils
import vytools.object
import vytools.episode
from vytools._actions import scan
import vytools.utils as utils
import logging
import asyncio
import random
import hashlib

from sanic import Sanic, response
from sanic_cors import CORS, cross_origin

BASEPATH = os.path.dirname(os.path.realpath(__file__))

def hash_request(dictx):
  return hashlib.sha1(json.dumps(dictx, sort_keys=True).encode()).hexdigest()

def parse(name, pth, reponame, items):
  item = {
    'name':name,
    'repo':reponame,
    'thingtype':'ui',
    'depends_on':[],
    'path':pth
  }
  return utils._add_item(item, items, True)

def find_all(items, contextpaths=None):
  success = utils.search_all(None, parse, items, is_ui=True, contextpaths=contextpaths)
  return success

def get_ui(req, items):
  ui_name = req.get('name','')
  ui = items.get(ui_name,None)
  loaded = {'html':'Could not find '+ui_name}
  if ui:
    loaded['name'] = ui_name
    loaded['html'] = Path(ui['path']).read_text()
  return loaded

def get_episode(req, items):
  episode_name = req.get('name','')
  episode = items.get(episode_name,{})
  loaded = {}
  if episode:
    loaded = get_compose({'name':episode.get('compose','')},items)
    loaded['name'] = episode_name
    obj = items.get(episode.get('data',''),None)
    if obj:
      loaded['calibration'] = vytools.object.expand(obj['data'],obj['definition'],items)
      loaded['definition'] = obj['definition']
  return loaded

def get_compose(req,items):
  compose_name = req.get('name','')
  compose = items.get(compose_name,{})
  loaded = {}
  if compose:
    loaded['name'] = compose_name
    loaded['html'] = 'Could not find '+compose.get('ui','')
    ui = items.get(compose.get('ui',''),None)
    if ui: loaded['html'] = Path(ui['path']).read_text()
  return loaded

def build_run(req, action, jobpath, items):
  try:
    kwargs = req['kwargs'] if 'kwargs' in req else {}
    if kwargs is None: kwargs = {}
    if 'jobpath' in kwargs: del kwargs['jobpath']
    if jobpath: kwargs['jobpath'] = jobpath
    # kwargs['items'] = items # TODO Add this if you every make items a keyword
    if action == 'build':
      vytools.build(req['list'],items,**kwargs)
    elif action == 'run':
      vytools.run(req['list'],items,**kwargs)
  except Exception as exc:
    vytools.printer.print_fail(str(exc))
    
def mimetype(pth):
  extensions_map = {
      '': 'application/octet-stream',
      '.manifest': 'text/cache-manifest',
      '.html': 'text/html',
      '.png': 'image/png',
      '.ico': 'image/ico',
      '.jpg': 'image/jpg',
      '.svg':	'image/svg+xml',
      '.css':	'text/css',
      '.js':'application/x-javascript',
      '.wasm': 'application/wasm',
      '.json': 'application/json',
      '.xml': 'application/xml',
  }
  return extensions_map.get('.'+pth.rsplit('.',1)[-1],'text/html')

class StatusMsg:

  def __init__(self, queue):
    self.messages = {}
    self.queue = queue

  async def add(self,topic,msg,level='info',timeout=None):
    id = random.randint(0,10000000)
    self.messages[topic] = {'message':msg,'level':level,'id':id}
    await self.queue.put(self.messages)
    if timeout:
      await asyncio.sleep(timeout)
      if topic in self.messages and self.messages[topic]['id'] == id:
        del self.messages[topic]
        await self.queue.put(self.messages)

  async def delete(self,topic):
    if topic in self.messages:
      del self.messages[topic]
      await self.queue.put(self.messages)

def server(items=None, jobpath=None, port=17171, subscribers=None, 
    menu = None, sockets=None, top_level=None, hide_log=False):
  
  rescannable = False
  if items is None: 
    rescannable = True
    items = ITEMS
  if subscribers is None: subscribers = {}
  if sockets is None: sockets = {}
  STATUSES = None
  THREAD = {}
  LOGSBUFFER = []
  vytools.printer.set_buffer(LOGSBUFFER)

  async def check_running():
    nonlocal THREAD, LOGSBUFFER
    while True:
      await asyncio.sleep(1)
      try:
        deletes = [key for key in THREAD if not THREAD[key].is_alive()]
        for key in deletes:
            del THREAD[key]
            await STATUSES.add(key,'Finished job','info',4)
      except Exception as exc:
        print(exc)

  async def logsbuffer(logsque):
    nonlocal LOGSBUFFER
    while True:
      while LOGSBUFFER:
        await logsque.put({'message':LOGSBUFFER.pop().strip('\n')})
      await asyncio.sleep(0.1)

  # logging.basicConfig(level=logging.DEBUG)
  resources={
    r"/vy/*": {"origins": "*"}
  }
  for x in items:
    if x.startswith('ui:'):
      vydir = x.split('/')[0].replace('ui:','',1)
      resources[r"/{}/*".format(vydir)] = {"origins": "*"}
  app = Sanic(__name__)
  CORS(app, resources, automatic_options=True)

  @app.listener('after_server_start')
  async def create_task_queue(app, loop):
      nonlocal STATUSES
      app.statusqueue = asyncio.Queue(loop=loop, maxsize=100)
      app.logsqueue = asyncio.Queue(loop=loop, maxsize=100)
      asyncio.create_task(logsbuffer(app.logsqueue))
      asyncio.create_task(check_running())
      STATUSES = StatusMsg(app.statusqueue)

  app.static('/', os.path.join(BASEPATH, 'base', 'main.html'))
  app.static('/favicon.ico', os.path.join(BASEPATH, 'base', 'favicon.ico'))
  app.static('/vy/base', os.path.join(BASEPATH, 'base'))

  @app.route('<tag:path>', methods=['GET', 'OPTIONS'])
  async def _app_things(request, tag):
    pth = items.get('ui:'+tag,{}).get('path',None)
    if pth:
      return await response.file(pth,headers={'Content-Type':mimetype(pth)})
    else:
      return response.empty()

  @app.post('/vy/subscribers/<tag>')
  async def _app_subscribers(request, tag):
    if tag in subscribers:
      return response.json(subscribers[tag](request.json) if tag in subscribers else {})
    return response.json({})

  for tag in sockets:
    app.add_websocket_route(sockets[tag], tag)

  @app.post('/vy/__<tag>__')
  async def _app_builtin(request, tag):
    nonlocal THREAD
    if tag == 'init':
      rslt = {
        'items':items,
        'server_subscribers':[k for k in subscribers.keys()],
        'menu':CONFIG.get('menu') if menu is None else menu,
        'hide_log':bool(hide_log)
      }
      if top_level is not None and top_level in items: rslt['top_level'] = top_level
      return response.json(rslt)
    elif tag == 'login':
      username = request.json.get('username')
      password = request.json.get('password')
      return response.json('User accounts are not yet enabled')
    elif tag == 'rescan':
      if rescannable:
        scan(contextpaths=CONFIG.get('scanned'))
      return response.json({'rescanned':rescannable})
    elif tag == 'stop':
      vytools.composerun.stop()
    elif tag == 'compose':
      return response.json(get_compose(request.json, items))
    elif tag == 'ui':
      return response.json(get_ui(request.json, items))
    elif tag == 'episode':
      return response.json(get_episode(request.json, items))
    elif tag == 'item':
      pth = items.get(request.json.get('name',None),{}).get('path',None)
      if pth: return await response.file(pth)
    elif tag in ['build','run']:
      starting = False
      key = 'job_'+hash_request(request.json)
      if key not in THREAD or not THREAD[key].is_alive():
        await STATUSES.add(key,'Started job, no more jobs will be accepted until this one finishes','info')
        THREAD[key] = threading.Thread(target=build_run, args=(request.json, tag, jobpath, items,), daemon=True)
        THREAD[key].start()
        starting = bool(THREAD[key])
      else:
        await STATUSES.add(key,'Wait until current job finishes','info')
      return response.json({'starting':starting})
    elif tag == 'menu':
      if menu is None: CONFIG.set('menu',request.json)
    elif tag == 'artifact':
      episode_name = request.json.get('name','')
      if episode_name.startswith('episode:'):
        artifact_name = request.json.get('artifact','_')
        apaths = vytools.episode.artifact_paths(episode_name, items, jobpath=jobpath)
        if artifact_name in apaths:
          return await response.file(apaths[artifact_name])
        else:
          logging.error('Could not find artifact {n} in {l}'.format(n=artifact_name,l=','.join(apaths)))
    return response.json({})

  @app.websocket('/vy/server_status')
  async def _app_server_status(request, ws):
    while True:
      msg = await app.statusqueue.get()
      await ws.send(json.dumps(msg))

  @app.websocket('/vy/logging')
  async def _app_logs(request, ws):
    while True:
      msg = await app.logsqueue.get()
      await ws.send(json.dumps(msg))

  try:
    app.run(host="0.0.0.0", port=port, debug=False, access_log=False)
    logging.info('Serving vytools on http://localhost:{p}'.format(p=port))
  except KeyboardInterrupt:
    # TODO shutdown running jobs?
    vytools.composerun.stop()
    print("Received exit, exiting.")
  