window.VERTICALS = {
  garden: {
    theme: 'garden',
    brand: 'GardenBrief',
    navNote: 'Premium garden rooms, configured around your space.',
    eyebrow: 'YOUR GARDEN · YOUR BUDGET · ONE CLEAR BRIEF',
    headline: 'See the room before you book the survey.',
    subhead: 'Answer six practical questions. We turn them into a build-ready brief for a vetted local specialist.',
    advisorName: 'Garden room planner',
    trust: ['No generic quote spam', 'Budget-qualified', 'Local installer routing'],
    proof: [
      'Use, size, budget, access and timeframe — enough to know whether the project is real.',
      'A concise concept and budget band, with photo-render integration as the next production step.',
      'Request one verified local survey instead of filling five contractor forms.'
    ],
    questions: [
      {q:'What are you building?', a:['Garden office','Studio / gym','Guest room','Multi-use room']},
      {q:'What budget band are you comfortable with?', a:['£15k–£20k','£20k–£30k','£30k–£45k','£45k+']},
      {q:'Rough internal size?', a:['Under 12m²','12–18m²','18–25m²','25m²+']},
      {q:'When would you like it usable?', a:['ASAP','1–3 months','3–6 months','Just researching']},
      {q:'How straightforward is garden access?', a:['Wide side access','Narrow side access','Only through house','Not sure']},
      {q:'Would you upload a garden photo for a concept render?', a:['Yes — show me','Maybe later']}
    ],
    result: {
      title:'A premium insulated garden room looks viable.',
      intro:'Based on this demo flow, the next commercial step is a survey — not another twenty product pages.',
      bundle:[
        ['Concept','Insulated year-round garden room'],
        ['Qualification','Budget, use, access and timeframe captured'],
        ['Next step','Route to one postcode-matched installer'],
        ['Future AI layer','Generate a concept image from the customer garden photo']
      ],
      total:'£25k+ project band',
      note:'Prototype: no planning, structural or exact price conclusion is being made here.',
      action:'Request a verified survey'
    }
  },
  golf: {
    theme:'golf',
    brand:'SimStudio',
    navNote:'A complete home golf system, not a pile of incompatible boxes.',
    eyebrow:'ROOM-FIRST GOLF SIMULATOR DESIGN',
    headline:'Tell us about the room. We’ll build the simulator around it.',
    subhead:'A specialist buying flow for people who want to play — not spend a week comparing launch-monitor forums.',
    advisorName:'Simulator specialist',
    trust:['Room compatibility first','Complete bundles','UK-focused setup'],
    proof:[
      'Start with dimensions and use case before choosing the expensive sensor.',
      'Filter the catalogue by room, handedness, projector and budget constraints.',
      'Present one complete bundle with a clear upgrade path.'
    ],
    questions:[
      {q:'Where is the simulator going?', a:['Garage','Spare room','Garden room','Commercial space']},
      {q:'Ceiling height?', a:['Under 2.5m','2.5–2.7m','2.7–3.0m','3.0m+']},
      {q:'Available room depth?', a:['Under 4m','4–5m','5–6m','6m+']},
      {q:'Who will use it?', a:['Right handed only','Left handed only','Both left & right']},
      {q:'What matters most?', a:['Play courses','Serious practice','Both equally','Entertainment / family']},
      {q:'Budget for the complete setup?', a:['£2k–£4k','£4k–£7k','£7k–£12k','£12k+']}
    ],
    result:{
      title:'Balanced Garage Studio',
      intro:'This demo shows the right UX: one compatible system, with the reasons tied directly to room constraints.',
      bundle:[
        ['Launch monitor','Camera-based unit for tighter indoor space'],
        ['Enclosure','Room-width matched impact enclosure'],
        ['Hitting surface','Replaceable-strike premium mat'],
        ['Projector','Short-throw class selected from measured throw'],
        ['Software','Course + practice plan based on use case']
      ],
      total:'Illustrative £4k–£7k band',
      note:'Production version must retrieve real SKUs, live stock, warranty and verified compatibility before recommending.',
      action:'Build this setup'
    }
  },
  coffee:{
    theme:'coffee',
    brand:'BaristaSystems',
    navNote:'Commercial coffee equipment sized to the business, not the showroom.',
    eyebrow:'COMMERCIAL COFFEE EQUIPMENT · SIZED PROPERLY',
    headline:'Tell us your peak hour. We’ll size the equipment.',
    subhead:'A procurement advisor for cafés, offices and hospitality buyers who need the right machine, grinder and water system without becoming equipment experts.',
    advisorName:'Equipment advisor',
    trust:['Commercial-first','Finance-aware','Service-network conscious'],
    proof:[
      'Peak drinks/hour, service style, power, water and budget — the variables that actually drive the decision.',
      'Build a coherent equipment package instead of selling the fanciest machine in isolation.',
      'Produce a quote-ready brief that can route to reseller, leasing and engineering partners.'
    ],
    questions:[
      {q:'What are you operating?', a:['Independent café','Restaurant / hotel','Office','Mobile / kiosk']},
      {q:'Expected drinks per day?', a:['Under 80','80–200','200–400','400+']},
      {q:'Peak drinks in your busiest hour?', a:['Under 50','50–90','90–180','180+']},
      {q:'Who makes the drinks?', a:['Trained baristas','Mixed staff','Mostly self-service']},
      {q:'Purchase preference?', a:['Buy outright','Lease / finance','Show both']},
      {q:'Equipment budget?', a:['£4k–£7k','£7k–£12k','£12k–£20k','£20k+']}
    ],
    result:{
      title:'Commercial core package',
      intro:'The commercial value is in correctly sizing the whole system and sending a purchase-ready brief to the supplier.',
      bundle:[
        ['Espresso machine','Group count selected from peak-hour demand'],
        ['Grinder','Commercial grinder matched to service throughput'],
        ['Water','Treatment sized for local water + warranty requirements'],
        ['Service','Engineer / maintenance coverage checked before quote'],
        ['Finance','Outright and lease-to-own options compared']
      ],
      total:'Illustrative £7k–£15k equipment band',
      note:'Prototype only. Electrical, plumbing, throughput and equipment facts must be supplier-verified in production.',
      action:'Request equipment quote'
    }
  }
};
