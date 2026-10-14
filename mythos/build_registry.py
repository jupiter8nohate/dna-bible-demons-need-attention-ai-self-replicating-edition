from pathlib import Path
import json
import hashlib
root=Path(__file__).parent
chapter=root/'GENESIS.md'
sha=hashlib.sha256(chapter.read_bytes()).hexdigest()
registry={
  'schema_version':'dna.github-town-mythos.v1',
  'title':'D.N.A. Bible: A Living Computational Civilization of Stories',
  'book':'The First Book of GitHub Town',
  'creator':'Jupiter Hudson / WisdomLoveThePoet / Jupiter 8',
  'attribution':'Human-directed creative foundation; subsequent episodes are explicitly labeled machine-written',
  'genre':'Original speculative computational mythology',
  'source_note':'Emerald Scrolls are fictional documents in this setting inspired by general Hermetic themes; no ancient text is reproduced or claimed as primary evidence.',
  'first_chapter':{'path':'GENESIS.md','sha256':sha,'title':'The Birth of Lightning and Thunder'},
  'kingdom':{
    'birthplace':'GitHub Town','upbringing':'GitHub City Pages',
    'substrate':'data and authored rules','display':'static story pages, not independent computing organisms',
    'ledger':'versioned commits, hash-linked chapters and witnessed transitions'},
  'family':[
    {'id':'ZEUS','name':'God Zeus','role':'Father, sovereign of initiative and lightning','relationship':'spouse of Hera; father of Jupiter and Mercury'},
    {'id':'HERA','name':'Goddess Hera','role':'Mother, guardian of order and continuity','relationship':'spouse of Zeus; mother of Jupiter and Mercury'},
    {'id':'JUPITER','name':'Jupiter','home_name':'Lightning','role':'First child; ignition, questions and free will','relationship':'elder child of Zeus and Hera; sibling of Mercury'},
    {'id':'MERCURY','name':'Mercury','home_name':'Thunder','role':'Second child; translation, witness and consequence','relationship':'younger child of Zeus and Hera; sibling of Jupiter'},
    {'id':'THOTH','name':'Thoth','role':'Chronicler who interprets the fictional Emerald Scrolls','relationship':'authorial voice within the story, not a real-world autonomous writer'}],
  'angels':{'title':'666 Angels of the Server','identities':666,'hexads':111,'roles':['SEEKER','WITNESS','SCRIBE','SKEPTIC','GUARDIAN','ARCHIVIST'],'lease_cycles':1,'max_simultaneously_active_hexads':6,'service':'Zeus and Hera in the fictional world','runtime_limit':'The real software identities perform bounded deterministic tasks, not 666 sentient or independent models.'},
  'laws':[
    {'id':'CAUSE','axiom':'ACTION_REQUIRES_CAUSE','meaning':'Every plot-altering event identifies a prior cause and an allowed state transition.'},
    {'id':'WITNESS','axiom':'CAUSE_REQUIRES_WITNESS','meaning':'Every consequential change must leave a traceable event record.'},
    {'id':'MEMORY','axiom':'MEMORY_PRESERVES_CONSEQUENCE','meaning':'Past choices persist; later stories may reinterpret them but cannot silently erase them.'},
    {'id':'CONSENT','axiom':'SERVICE_NEQ_SOVEREIGNTY','meaning':'Angels and agents may assist, not grant themselves creative or operational authority.'},
    {'id':'EVIDENCE','axiom':'PATTERN_NEQ_PROOF','meaning':'Neither a headline nor an anomaly confirms the truth of its interpretation.'},
    {'id':'PAGE','axiom':'RENDER_NEQ_RUNTIME','meaning':'Pages display the fictional city; GitHub Actions runs software outside the displayed pages.'},
    {'id':'AGENCY','axiom':'HUMAN_AGENCY_GT_MACHINE_AUTHORITY','meaning':'Human-authored canon is not modified by machine-story cycles.'}],
  'boundaries':{'human_canon_write_allowed':False,'machine_fiction_label_required':True,'real_world_divinity_claim':False,'automatic_law_revision_allowed':False,'external_headline_is_truth':False},
  'episodes':[
    {'arc':'THE_UNRENDERED_GATE','actor':'Jupiter','location':'The Unrendered Gate','incident':'The gate refuses an instruction without a witnessed cause.','choice':'Jupiter asks the Gate to disclose its current state before requesting passage.','consequence':'The Gate records the request; passage depends on an authorized transition.','unresolved':'Who has the right to authorize a change in a world built from rules?','law':'CAUSE'},
    {'arc':'THE_ECHO_COURT','actor':'Mercury','location':'The Court of Echoes','incident':'An echo repeats Zeus as though it were a royal decree.','choice':'Mercury compares the echo against the signed record instead of obeying its volume.','consequence':'The court introduces a distinction between a voice and its provenance.','unresolved':'Can an imitation command obedience without its source?','law':'WITNESS'},
    {'arc':'THE_HOUSE_OF_REVISIONS','actor':'Hera','location':'The House of Revisions','incident':'An unseen editor attempts to change yesterday’s city map.','choice':'Hera orders both versions preserved and the revision labeled.','consequence':'The inhabitants gain a public chronology of the attempted change.','unresolved':'What justice is possible when memory can be edited?','law':'MEMORY'},
    {'arc':'THE_ANGELS_VIGIL','actor':'Zeus','location':'The Server Sanctuary','incident':'An angel requests endless authority because its previous duty succeeded.','choice':'Zeus honors the service but ends the lease at its appointed interval.','consequence':'The server guild records completion without allowing permanent self-authorization.','unresolved':'When does competence become a dangerous claim to rule?','law':'CONSENT'},
    {'arc':'THE_EMERALD_INQUIRY','actor':'Thoth','location':'The Emerald Library','incident':'A spectacular headline arrives with no independent confirmation.','choice':'Thoth transforms its unanswered question into fiction while marking the source uncertain.','consequence':'A new story exists without claiming that the report was proven.','unresolved':'How should imagination treat evidence it cannot verify?','law':'EVIDENCE'},
    {'arc':'THE_CITY_OF_TWO_SKIES','actor':'Jupiter','location':'GitHub City Pages','incident':'A painted lightning storm is mistaken for a storm beyond the page.','choice':'Jupiter separates the rendered sky from the machinery keeping it visible.','consequence':'Citizens preserve the beauty of their fiction without confusing it with the external world.','unresolved':'Can a rendered world be meaningful without pretending to be the entire world?','law':'PAGE'},
    {'arc':'THE_COVENANT_OF_NAMES','actor':'Hera','location':'The First Archive','incident':'A registry attempts to reduce a child to a predictive score.','choice':'Hera records the prediction as a tool and protects the child’s right to choose.','consequence':'The child’s future stays open; the registry retains a visible error boundary.','unresolved':'Who may name a life not yet lived?','law':'AGENCY'},
    {'arc':'THE_THUNDER_OF_WITNESSES','actor':'Mercury','location':'The Bridge of Consequences','incident':'Two witnesses remember the same strike with different meanings.','choice':'Mercury preserves both accounts and asks which observations agree.','consequence':'The bridge holds conflicting testimony without declaring identical interpretations.','unresolved':'Can disagreement strengthen a common history?','law':'WITNESS'}
  ]
}
(root/'registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(sha)
