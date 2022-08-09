server_url = 'grpcs://dalle-flow.dev.jina.ai'

import requests, datetime, sys
from random import randrange

for _ in range(int(sys.argv[1])):

  styles = requests.get("https://gist.github.com/doteater/a5f70e6560e6c3af202c8adcda9dc47a/raw")
  subjects = requests.get("https://gist.github.com/doteater/fd36f350e3b2c8a358b1260ef0f2c6bd/raw")
  styles = styles.text.split("\n")
  subjects = subjects.text.split("\n")
  style = styles[randrange(len(styles)-1)]
  subject = subjects[randrange(len(subjects)-1)]
  print(f'prompt: {style} {subject}')
  prompt = f'{style} {subject}'




  from docarray import Document
  
  print('rendering...')
  da = Document(text=prompt).post(server_url, parameters={'num_images': 1}).matches

  #da.plot_image_sprites(fig_size=(10,10), show_index=True)



  fav_id = 0

  fav = da[fav_id]

  #fav.display()


  print('diffusing...')
  diffused = fav.post(f'{server_url}', parameters={'skip_rate': 0.6, 'num_images': 1}, target_executor='diffusion').matches

  #diffused.plot_image_sprites(fig_size=(10,10), show_index=True)



  dfav_id = 0

  fav = diffused[dfav_id]

  #fav.display()



  
  print('upscaling...')
  fav = fav.post(f'{server_url}/upscale')
  fav.save_uri_to_file(f'output/{style} {subject}-{datetime.datetime.now()}.png')
  
  print(f'done! inspect the gem: output/{style} {subject}-{datetime.datetime.now()}.png')
