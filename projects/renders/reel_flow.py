"""Centro Equino stable reel from Google Flow clips (6 Oct 2026, Will: 'a full set of animated clips ... focus mostly on the
main stable; walk through, night, sunrise, sunset, people enjoying wine, kids playing'). Made in Flow (Veo 3.1 Quality, Will's
AI Pro credits) from paintings of the current model; downloaded clips are copied into anim-flow/ under scene names.

    python reel_flow.py            (picks up the clips in anim-flow/, in SCENES order; missing ones are skipped)
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, 'anim-flow')
sys.argv = [sys.argv[0]]
import reel as R

SCENES = ['01-sunrise', '02-walkthrough', '03-kids', '04-wine', '05-night']   # current-model clips, a day at the stable

if __name__ == '__main__':
    clips = [os.path.join(A, s + '.mp4') for s in SCENES if os.path.exists(os.path.join(A, s + '.mp4'))]
    print('clips:', [os.path.basename(c) for c in clips])
    t0, t1 = os.path.join(A, '00-title.mp4'), os.path.join(A, '99-end.mp4')
    R.title(t0, 'El establo', 'Centro Equino · Chichihuas'); R.title(t1, 'Centro Equino', 'diseño preliminar · preliminary design · 2026')
    R.A = A
    R.assemble([t0] + clips + [t1], os.path.join(A, 'centro-equino-stable-reel.mp4'))
