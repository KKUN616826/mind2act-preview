from pathlib import Path
import json,collections
base=Path('.production/clarity-montage-20261011-114333')
x=json.loads((base/'animation-map/animation-map.json').read_text())
tweens=x['tweens']
flag_names=sorted({f for t in tweens for f in t['flags']})
counts=collections.Counter(f for t in tweens for f in t['flags'])
indices={f:[i for i,t in enumerate(tweens) if f in t['flags']] for f in flag_names}
def refs(ids):
 return [{'map_index':i,'selector':tweens[i]['selector'],'start':tweens[i]['start'],'end':tweens[i]['end'],'props':tweens[i]['props']} for i in ids]
category_rationale={
'intro':'Full-screen footage mosaics deliberately overlap in a staged reveal; separate Mind/Act assets and dots converge before the exact complete logo replaces them. Title band and its clipped bitmap are intentional parent/child overlaps.',
'motivation':'A full-screen surface contains the three aligned category groups, names and descriptions. Parent/child bounding boxes and repeated enumeration are not text collisions.',
'mind':'Footage camera, lower title band, memory inset and its labels are intentionally layered; camera zoom is a slow background motion.',
'memory':'Memory inset frame/content is an intentional overlay on the actual task footage.',
'act':'Real action camera and target focus/inset overlays are layered to show the tracing task. Three physical-execution lines stay inside their floating card.',
'mind2act':'Piano camera and related task/sequence overlays form the retained case layout.',
'piano':'Sequence excerpt, notes and phase indicators deliberately overlap their inset container. Short fades separate annotation states.',
'coord':'Arrows and labels coexist with original symbols. Conceptual combination intentionally overlaps separate symbols and dots with the complete exact brand asset during a brief crossfade. Pulse bounding boxes cover the whole SVG arc although only an 11% segment is painted; root/nested duplicate entries inflate collision flags.',
'scale':'Fullscreen case surfaces and bottom title bars overlap deliberately. CP04 is one continuous video shrinking into its CP04 card while the three-column task wall appears; its thumbnail area is intentionally reserved, avoiding duplicate media.',
'outro':'Flight path, logo, expanding wordmark band, accent and CTA are intentional layers with readable final hold.',
'difficulty':'Easy/Medium/Hard text and CP02 still/cover pairs use intentional replacements. Hard hero shrinks into its reserved grid slot. Grid card/label/frame overlaps and 45-stat payoff replacement are intentional.'}
def family(selector):
 s=selector.lstrip('#')
 if s.startswith('div.'):s=s[4:]
 return s.split('-')[0]
collision_groups=[]
for prefix in sorted({family(tweens[i]['selector']) for i in indices['collision']}):
 ids=[i for i in indices['collision'] if family(tweens[i]['selector'])==prefix]
 collision_groups.append({'family':prefix,'count':len(ids),'indices':ids,'classification':'intentional_layering_or_duplicate_enumeration','rationale':category_rationale[prefix]})
# Every special flag is accounted for, including the handful at correct global time.
invisible_groups=[
 {'indices':[92,93,97,98,117,119], 'rationale':'Intro assets are sampled on duplicate +0.671 s entries after the intentional complete-logo crossfade. Correct original entries at 1.90–2.61 s show the convergence/replacement.'},
 {'indices':[250,315,324,333,366,421,422,425,433,434,437,455,459,460,462,463,501], 'rationale':'Duplicate entries are sampled 0.671 s after the actual tween. Fade-outs have already completed or the true hero handoff has already ended. Example: return pulse actual 32.48–33.53 s is duplicated at 33.151–34.201 s; the map does not represent a second playback.'},
 {'indices':[443,444], 'rationale':'The collective difficulty handoff fades all three descriptions; Easy and Medium were intentionally already hidden by the preceding level changes. These zero-change members do not affect the active Hard description or playback.'}
]
assert sorted(i for g in invisible_groups for i in g['indices'])==indices['invisible']
report={
 'status':'reviewed_no_additional_source_change_required',
 'scope':'Animation-map heuristics and current HyperFrames screenshots. Final encoded visual review is performed separately by root.',
 'map':'animation-map/animation-map.json',
 'totals':{k:x[k] for k in ['duration','totalTweens','mappedTweens','skippedMicroTweens']},
 'flag_counts':dict(counts),
 'tool_limitations':{
  'enumeration':'animation-map.mjs walks getChildren(true,true,true) recursively and separately walks every registered timeline, without object-identity deduplication. The map therefore includes local and global versions of the same tween and extra +0.671 s copies.',
  'concrete_duplicate_examples':refs([71,300,304,128,306,308,158,356,367,41,490,496]),
  'collision':'Only time-proximate bounding-box overlap (>30% of one box) is tested; ancestry, masking, alpha coverage and intentional compositing are not excluded.',
  'visibility':'Bounding boxes from timelines sampled outside their owning scene can be zero/inactive, and late duplicate samples can be fully faded.',
  'pacing':'Thresholds flag duration below 0.2 s or above 2 s regardless of role. They are stylistic review prompts, not runtime failures.'
 },
 'flag_groups':{
  'collision':collision_groups,
  'invisible':invisible_groups,
  'offscreen':[
   {'indices':[17,79], 'rationale':'Scale hero title bar/type sampled at erroneous local-time entries while scale is inactive. The same elements are fully visible in the actual 42.25/43.90 s frames.'},
   {'indices':[41], 'rationale':'Outro accent is sampled at 1.331–1.941 s although outro starts 66.085185 s. Its initial scaleX=0 produces a zero-width inactive box. Correct actual 66.745–67.355 s entry and ending screenshot show the full accent.'},
   {'indices':[344], 'rationale':'Intentional 0.45 s entrance from below the frame: bar moves upward by 160 px and settles at y=922 with height=158, exactly ending at 1080. No persistent cropping.'}
  ],
  'degenerate':[{'indices':[41],'rationale':'Same inactive local-time outro accent sample described above, not a zero-width final accent.'}],
  'paced-slow':[{'indices':indices['paced-slow'],'rationale':'All nine entries are repeats of the three real-footage camera moves: Mind 2.15 s, Act 3.10 s and Mind2Act 2.65 s. Slow reframing preserves a readable view of physical execution; no narrative hold problem.'}],
  'paced-fast':[{'indices':indices['paced-fast'],'rationale':'All 35 entries animate opacity (alone or with a small auxiliary motion) over 0.15–0.19 s. They are focus/annotation fades, adjacent level swaps, grid label reveals and the exact-logo crossfade, not the total reading time. Stable states persist after each entrance. No high-velocity subject motion is required by these flags.'}]
 },
 'dead_zone_review':[
  {'start':10,'end':11,'classification':'intentional_reading_hold','rationale':'Three-category insight text remains stable for reading before first case.'},
  {'start':39.5,'end':41,'classification':'intentional_reading_hold','rationale':'Completed three-logo taxonomy holds before breadth montage.'},
  {'start':45.5,'end':46.5,'classification':'live_video_not_GSAP_motion','rationale':'CP04 real recipe execution is full-screen and playing before its shared-video shrink.'},
  {'start':49,'end':52,'classification':'live_video_plus_taxonomy_reading_hold','rationale':'Fifteen task thumbnail videos continue, while fixed category names provide a readable overview.'},
  {'start':71,'end':75,'classification':'intentional_final_hold','rationale':'Logo, CTA and URL remain onscreen long enough to read; user explicitly requested this hold.'}
 ],
 'changed_scene_visual_review':{
  '08-coordination':{'result':'pass_in_HyperFrames_snapshots','evidence':['arrow-after/contact-sheet-1.jpg','arrow-after/contact-sheet-2.jpg','arrow-dom-after.json'],'observed':'Forward bright segment traverses Mind→Act, then lower segment traverses Act→Mind continuously. Fractional offset samples are preserved and the segment does not repeat at its origin.'},
  '06-scale':{'result':'pass_in_HyperFrames_snapshots','evidence':['montage-after/contact-sheet.jpg','montage-review.json'],'observed':'42.25 s M/Mind, 43.90 s FR1/Act, 45.25 s CP04/Mind2Act. At 47.80 s the shared CP04 video occupies its fourth-row Mind2Act thumbnail and all 15 task cards are present. At 52.70 s CP02 outline points to the following difficulty hero.'}
 },
 'unresolved_animation_findings':[],
 'final_render_gate':'Check actual encoded arrow samples 32.60,32.85,33.10,33.30,33.53 s and CP04 shrink continuity around46.60–47.70 s after full export.'
}
(base/'animation-review.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':report['status'],'flag_counts':report['flag_counts'],'all_flag_groups_accounted_for':True,'output':str(base/'animation-review.json')},ensure_ascii=False))
