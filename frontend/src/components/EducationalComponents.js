// Educational components for ML learning
import React, { useState } from 'react';

// Code explanation component
export const CodeExplanation = ({ concept, code, explanation }) => {
  const [showCode, setShowCode] = useState(false);

  return (
    <div className="bg-white/5 rounded-lg p-4 mb-4 border border-white/10">
      <div className="flex justify-between items-center mb-2">
        <h4 className="text-lg font-semibold text-white">{concept}</h4>
        <button
          onClick={() => setShowCode(!showCode)}
          className="text-blue-300 hover:text-blue-100 text-sm"
        >
          {showCode ? 'Hide' : 'Show'} Code
        </button>
      </div>
      <p className="text-blue-200 text-sm mb-3">{explanation}</p>
      {showCode && (
        <pre className="bg-black/40 p-3 rounded text-green-300 text-xs overflow-x-auto">
          <code>{code}</code>
        </pre>
      )}
    </div>
  );
};

// Interactive formula component
export const FormulaCard = ({ title, formula, variables, example }) => {
  return (
    <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 rounded-lg p-5 border border-purple-500/30">
      <h4 className="text-white font-bold mb-3">{title}</h4>
      <div className="bg-black/30 p-3 rounded mb-3 font-mono text-yellow-300 text-center">
        {formula}
      </div>
      {variables && (
        <div className="space-y-1 mb-3">
          <div className="text-blue-200 text-sm font-semibold">Where:</div>
          {variables.map((v, i) => (
            <div key={i} className="text-blue-200 text-xs">
              <span className="font-mono text-yellow-300">{v.symbol}</span> = {v.meaning}
            </div>
          ))}
        </div>
      )}
      {example && (
        <div className="text-blue-200 text-xs bg-white/5 p-2 rounded">
          <span className="font-semibold">Example:</span> {example}
        </div>
      )}
    </div>
  );
};

// Metric card with interpretation
export const MetricCard = ({ label, value, unit, interpretation, color = 'blue' }) => {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
    orange: 'from-orange-500 to-orange-600',
    red: 'from-red-500 to-red-600'
  };

  return (
    <div className="bg-white/10 rounded-lg p-4 border border-white/20">
      <div className="text-sm text-blue-200 mb-1">{label}</div>
      <div className={`text-3xl font-bold bg-gradient-to-r ${colorClasses[color]} text-transparent bg-clip-text`}>
        {value}{unit}
      </div>
      {interpretation && (
        <div className="text-xs text-blue-300 mt-2">{interpretation}</div>
      )}
    </div>
  );
};

// Visual chart placeholder
export const ChartPlaceholder = ({ title, description }) => {
  return (
    <div className="bg-white/5 rounded-lg p-6 border border-white/10 text-center">
      <div className="text-6xl mb-3">📊</div>
      <h4 className="text-white font-semibold mb-2">{title}</h4>
      <p className="text-blue-300 text-sm">{description}</p>
      <div className="mt-4 text-xs text-blue-400">
        💡 Tip: Check backend code to see how this data is computed
      </div>
    </div>
  );
};

// Learning objectives card
export const LearningObjectives = ({ objectives }) => {
  return (
    <div className="bg-gradient-to-br from-green-900/40 to-emerald-900/40 rounded-lg p-5 border border-green-500/30 mb-6">
      <h3 className="text-white font-bold mb-3 flex items-center gap-2">
        <span>🎯</span> What You'll Learn
      </h3>
      <ul className="space-y-2">
        {objectives.map((obj, i) => (
          <li key={i} className="text-blue-100 text-sm flex items-start gap-2">
            <span className="text-green-400 flex-shrink-0">✓</span>
            <span>{obj}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

// Code walkthrough stepper
export const CodeWalkthrough = ({ steps }) => {
  const [currentStep, setCurrentStep] = useState(0);

  return (
    <div className="bg-white/5 rounded-lg p-5 border border-white/10">
      <h3 className="text-white font-bold mb-4">Code Walkthrough</h3>
      
      {/* Progress */}
      <div className="flex gap-2 mb-4">
        {steps.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrentStep(i)}
            className={`flex-1 h-2 rounded ${
              i === currentStep
                ? 'bg-blue-500'
                : i < currentStep
                ? 'bg-blue-300'
                : 'bg-white/20'
            }`}
          />
        ))}
      </div>

      {/* Current step */}
      <div className="mb-4">
        <div className="text-blue-300 text-sm mb-2">
          Step {currentStep + 1} of {steps.length}
        </div>
        <h4 className="text-white font-semibold mb-2">{steps[currentStep].title}</h4>
        <p className="text-blue-200 text-sm mb-3">{steps[currentStep].description}</p>
        {steps[currentStep].code && (
          <pre className="bg-black/40 p-3 rounded text-green-300 text-xs overflow-x-auto">
            <code>{steps[currentStep].code}</code>
          </pre>
        )}
      </div>

      {/* Navigation */}
      <div className="flex gap-2">
        <button
          onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
          disabled={currentStep === 0}
          className="px-4 py-2 bg-white/10 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <button
          onClick={() => setCurrentStep(Math.min(steps.length - 1, currentStep + 1))}
          disabled={currentStep === steps.length - 1}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  );
};

// Concept explainer
export const ConceptExplainer = ({ concept, simpleExplanation, technicalExplanation, realWorldAnalogy }) => {
  const [mode, setMode] = useState('simple');

  return (
    <div className="bg-white/5 rounded-lg p-5 border border-white/10 mb-4">
      <div className="flex justify-between items-center mb-3">
        <h4 className="text-white font-bold">{concept}</h4>
        <div className="flex gap-2 text-xs">
          <button
            onClick={() => setMode('simple')}
            className={`px-3 py-1 rounded ${mode === 'simple' ? 'bg-blue-500 text-white' : 'bg-white/10 text-blue-300'}`}
          >
            Simple
          </button>
          <button
            onClick={() => setMode('technical')}
            className={`px-3 py-1 rounded ${mode === 'technical' ? 'bg-blue-500 text-white' : 'bg-white/10 text-blue-300'}`}
          >
            Technical
          </button>
          <button
            onClick={() => setMode('analogy')}
            className={`px-3 py-1 rounded ${mode === 'analogy' ? 'bg-blue-500 text-white' : 'bg-white/10 text-blue-300'}`}
          >
            Analogy
          </button>
        </div>
      </div>
      
      <div className="text-blue-200 text-sm">
        {mode === 'simple' && simpleExplanation}
        {mode === 'technical' && technicalExplanation}
        {mode === 'analogy' && realWorldAnalogy}
      </div>
    </div>
  );
};

// Quiz component
export const QuickQuiz = ({ question, options, correctAnswer, explanation }) => {
  const [selected, setSelected] = useState(null);
  const [showResult, setShowResult] = useState(false);

  const handleSubmit = () => {
    setShowResult(true);
  };

  const reset = () => {
    setSelected(null);
    setShowResult(false);
  };

  return (
    <div className="bg-gradient-to-br from-indigo-900/40 to-purple-900/40 rounded-lg p-5 border border-indigo-500/30">
      <h4 className="text-white font-bold mb-3 flex items-center gap-2">
        <span>🧠</span> Quick Quiz
      </h4>
      <p className="text-blue-100 mb-4">{question}</p>
      
      <div className="space-y-2 mb-4">
        {options.map((option, i) => (
          <button
            key={i}
            onClick={() => !showResult && setSelected(i)}
            disabled={showResult}
            className={`w-full text-left p-3 rounded border transition-all ${
              showResult
                ? i === correctAnswer
                  ? 'bg-green-500/30 border-green-500 text-white'
                  : i === selected
                  ? 'bg-red-500/30 border-red-500 text-white'
                  : 'bg-white/5 border-white/10 text-blue-300'
                : selected === i
                ? 'bg-blue-500/30 border-blue-500 text-white'
                : 'bg-white/5 border-white/10 text-blue-200 hover:bg-white/10'
            }`}
          >
            {option}
          </button>
        ))}
      </div>

      {!showResult ? (
        <button
          onClick={handleSubmit}
          disabled={selected === null}
          className="w-full py-2 bg-blue-500 text-white rounded disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Submit Answer
        </button>
      ) : (
        <div>
          <div className={`p-3 rounded mb-3 ${
            selected === correctAnswer
              ? 'bg-green-500/20 border border-green-500/50 text-green-100'
              : 'bg-red-500/20 border border-red-500/50 text-red-100'
          }`}>
            {selected === correctAnswer ? '✅ Correct!' : '❌ Incorrect'}
            <div className="text-sm mt-2 opacity-90">{explanation}</div>
          </div>
          <button
            onClick={reset}
            className="w-full py-2 bg-white/10 text-white rounded hover:bg-white/20"
          >
            Try Again
          </button>
        </div>
      )}
    </div>
  );
};

// File reference card
export const FileReference = ({ filename, description, keyFunctions }) => {
  return (
    <div className="bg-white/5 rounded-lg p-4 border border-white/10 mb-4">
      <div className="flex items-center gap-2 mb-2">
        <span className="text-2xl">📝</span>
        <code className="text-blue-300 font-semibold">{filename}</code>
      </div>
      <p className="text-blue-200 text-sm mb-3">{description}</p>
      {keyFunctions && keyFunctions.length > 0 && (
        <div>
          <div className="text-xs text-blue-300 mb-2">Key Functions:</div>
          <div className="flex flex-wrap gap-2">
            {keyFunctions.map((fn, i) => (
              <code key={i} className="text-xs bg-black/30 px-2 py-1 rounded text-green-300">
                {fn}
              </code>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default {
  CodeExplanation,
  FormulaCard,
  MetricCard,
  ChartPlaceholder,
  LearningObjectives,
  CodeWalkthrough,
  ConceptExplainer,
  QuickQuiz,
  FileReference
};