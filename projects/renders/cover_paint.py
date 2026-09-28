"""Repaint the pack cover (the 'from the hill' view) from the current model, keeping the look of Will's chosen painting."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import paint
from paint import openai, google, key
from gallery2 import gemini_key
from gallery3 import BRIEF
paint.QUAL = 'high'
EXTRA = (' The FIRST image is the exact model render: its camera, terrain and every building, roof, fence, road and trough position are the truth. '
         'The SECOND image is only a style reference: match its golden-hour light, sky with big lit clouds, colours, vegetation, horses and people. '
         'Do not copy anything built from the second image: in particular the round water trough is low tan fieldstone under the end of the '
         'butterfly roof chute (no metal tank, no downspout pipe), and the trailer has a wooden deck with three curved stepped platforms in front of it, '
         'not straight bleachers.')
eng = sys.argv[1]; k = key('OPENAI_API_KEY') if eng == 'openai' else gemini_key()
im = (openai if eng == 'openai' else google)(os.path.join(HERE, 'model', 'model-25b-cover.png'), BRIEF + EXTRA, [os.path.join(HERE, 'cover-style-ref.jpg')], k)
im.save(os.path.join(HERE, 'gallery3', f'cover-hill-{eng}.png')); print(eng, 'ok')
