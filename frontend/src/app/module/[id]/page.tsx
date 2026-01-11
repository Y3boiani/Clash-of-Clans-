import Link from 'next/link'

const modules = [
  {
    num: 1,
    title: 'Leadership Entropy',
    desc: 'Analyze clan leadership structure using Shannon Entropy and network analysis',
    concepts: ['Shannon Entropy', 'Influence Measurement', 'Bayesian Estimation'],
    file: 'ml_module_1_leadership.py'
  },
  {
    num: 2,
    title: 'Pressure Function',
    desc: 'Model player performance under high-pressure war situations',
    concepts: ['Gaussian Processes', 'Variance Analysis', 'Beta Distribution'],
    file: 'ml_module_2_pressure.py'
  },
  {
    num: 3,
    title: 'Coordination Analysis',
    desc: 'Detect emergent coordination patterns in war attack timing',
    concepts: ['Point Processes', 'Hidden Markov Models', 'Motif Detection'],
    file: 'ml_module_3_coordination.py'
  },
  {
    num: 4,
    title: 'Trophy Volatility',
    desc: 'Model trophy dynamics using stochastic differential equations',
    concepts: ['Ornstein-Uhlenbeck Process', 'Kalman Filter', 'Monte Carlo'],
    file: 'ml_module_4_volatility.py'
  },
  {
    num: 5,
    title: 'Donation Networks',
    desc: 'Analyze resource flow as a directed graph economy',
    concepts: ['Graph Theory', 'Gini Coefficient', 'PageRank'],
    file: 'ml_module_5_donations.py'
  },
  {
    num: 6,
    title: 'Capital Investment',
    desc: 'Model clan capital as a public goods game',
    concepts: ['Game Theory', 'Free-Rider Detection', 'Causal Inference'],
    file: 'ml_module_6_capital.py'
  },
  {
    num: 7,
    title: 'Matchmaking Fairness',
    desc: 'Audit war matchmaking for systematic biases',
    concepts: ['Demographic Parity', 'Propensity Scores', 'Fairness Metrics'],
    file: 'ml_module_7_fairness.py'
  }
]

export default async function ModulePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const moduleNum = parseInt(id)
  const module = modules.find(m => m.num === moduleNum)

  if (!module) {
    return (
      <div className="min-h-screen bg-coc-dark coc-wood-bg flex items-center justify-center">
        <div className="coc-card p-8 text-center">
          <h1 className="text-3xl font-bold text-red-400 mb-4">Module Not Found</h1>
          <Link href="/" className="coc-button px-6 py-3">
            Return Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-coc-dark coc-wood-bg">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <Link href="/" className="text-coc-gold hover:text-yellow-300 mb-8 inline-block">
          ← Back to Home
        </Link>
        
        <div className="coc-card p-8 border-4 mb-8">
          <h1 className="text-4xl font-bold text-coc-gold mb-2 gold-shine">
            Module {module.num}: {module.title}
          </h1>
          <p className="text-xl text-yellow-200 mb-6">{module.desc}</p>
          
          <div className="flex flex-wrap gap-2 mb-6">
            {module.concepts.map((concept, idx) => (
              <span key={idx} className="text-sm bg-gradient-to-r from-amber-900 to-amber-800 px-4 py-2 rounded-full text-yellow-100 border border-amber-700">
                {concept}
              </span>
            ))}
          </div>
          
          <div className="bg-black/30 p-4 rounded-lg">
            <div className="text-yellow-200 text-sm mb-2">Source Code:</div>
            <code className="text-green-400 font-mono">/app/backend/{module.file}</code>
          </div>
        </div>

        <div className="coc-card p-8 border-4">
          <h2 className="text-2xl font-bold text-coc-gold mb-4">📚 Learning Resources</h2>
          <div className="space-y-4 text-yellow-200">
            <p>
              This module demonstrates advanced ML concepts. To learn more:
            </p>
            <ol className="list-decimal list-inside space-y-2">
              <li>Read the source code in the backend directory</li>
              <li>Check the inline comments explaining each algorithm</li>
              <li>Run the analysis on your own clan data</li>
              <li>Modify parameters and observe the results</li>
            </ol>
          </div>
          
          <div className="mt-6">
            <Link href="/unified-dashboard" className="coc-button px-6 py-3">
              📊 View Live Analysis
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
