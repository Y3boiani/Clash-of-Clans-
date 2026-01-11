'use client'

import { useState, useEffect } from 'react'

// ==========================================
// Leadership Network Visualization
// ==========================================
interface Leader {
  player_name?: string
  influence_score?: number
  rank?: number
  formal_role?: string
}

interface LeadershipNetworkProps {
  leaders?: Leader[]
  entropy?: number
  leadershipType?: string
}

export function LeadershipNetwork({ leaders = [], entropy = 0, leadershipType = 'unknown' }: LeadershipNetworkProps) {
  const [animationStep, setAnimationStep] = useState(0)
  const topLeaders = leaders.slice(0, 7)
  
  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationStep(prev => (prev + 1) % 100)
    }, 50)
    return () => clearInterval(interval)
  }, [])

  const centerX = 150
  const centerY = 80
  
  const getNodePosition = (index: number, total: number) => {
    if (index === 0) return { x: centerX, y: centerY }
    const angle = ((index - 1) / (total - 1)) * Math.PI + Math.PI
    const radius = 60 + (index * 8)
    return {
      x: centerX + Math.cos(angle - Math.PI/2) * radius * 0.8,
      y: centerY + Math.sin(angle - Math.PI/2) * radius * 0.6 + 40
    }
  }

  return (
    <div className="leadership-viz">
      <svg viewBox="0 0 300 200" className="w-full h-48">
        <defs>
          <radialGradient id="nodeGradient" cx="50%" cy="30%" r="70%">
            <stop offset="0%" stopColor="#ffd700" />
            <stop offset="100%" stopColor="#8b6914" />
          </radialGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
          <linearGradient id="connectionGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ffd700" stopOpacity={0.8} />
            <stop offset={`${animationStep}%`} stopColor="#ff8c00" stopOpacity={1} />
            <stop offset="100%" stopColor="#ffd700" stopOpacity={0.3} />
          </linearGradient>
        </defs>
        
        {topLeaders.slice(1).map((_, index) => {
          const leaderPos = getNodePosition(0, topLeaders.length)
          const memberPos = getNodePosition(index + 1, topLeaders.length)
          return (
            <line
              key={`line-${index}`}
              x1={leaderPos.x}
              y1={leaderPos.y}
              x2={memberPos.x}
              y2={memberPos.y}
              stroke="url(#connectionGradient)"
              strokeWidth="2"
              strokeDasharray="5,3"
              opacity={0.6 + (topLeaders[index + 1]?.influence_score || 0.5) * 0.4}
            />
          )
        })}
        
        {topLeaders.slice(0, 3).map((leader, index) => {
          const pos = getNodePosition(index, topLeaders.length)
          const pulseRadius = 15 + (animationStep % 30)
          return (
            <circle
              key={`pulse-${index}`}
              cx={pos.x}
              cy={pos.y}
              r={pulseRadius}
              fill="none"
              stroke="#ffd700"
              strokeWidth="1"
              opacity={1 - (animationStep % 30) / 30}
            />
          )
        })}
        
        {topLeaders.map((leader, index) => {
          const pos = getNodePosition(index, topLeaders.length)
          const size = index === 0 ? 18 : 12 - index
          return (
            <g key={`node-${index}`} filter={index === 0 ? "url(#glow)" : undefined}>
              <circle
                cx={pos.x}
                cy={pos.y}
                r={size}
                fill="url(#nodeGradient)"
                stroke="#ffd700"
                strokeWidth={index === 0 ? 3 : 1.5}
              />
              {index === 0 && (
                <text x={pos.x} y={pos.y - 25} textAnchor="middle" fill="#ffd700" fontSize="10" fontWeight="bold">
                  👑
                </text>
              )}
              <text x={pos.x} y={pos.y + size + 12} textAnchor="middle" fill="#ffeeba" fontSize="8">
                {leader.player_name?.substring(0, 8) || `Player ${index + 1}`}
              </text>
            </g>
          )
        })}
        
        <g transform="translate(240, 20)">
          <rect x="0" y="0" width="50" height="40" rx="5" fill="rgba(0,0,0,0.5)" stroke="#8b6914" />
          <text x="25" y="15" textAnchor="middle" fill="#ffd700" fontSize="8" fontWeight="bold">ENTROPY</text>
          <text x="25" y="32" textAnchor="middle" fill="#ff8c00" fontSize="12" fontWeight="bold">
            {entropy?.toFixed(2) || '0.00'}
          </text>
        </g>
      </svg>
      
      <div className="text-center mt-2">
        <span className="text-xs text-yellow-200 uppercase tracking-wider">
          Structure: <span className="text-coc-gold font-bold">{leadershipType}</span>
        </span>
      </div>
    </div>
  )
}

// ==========================================
// Donation Flow Visualization
// ==========================================
interface Contributor {
  player_name?: string
  donations_given?: number
}

interface DonationFlowVizProps {
  contributors?: Contributor[]
  parasites?: number
  healthGrade?: string
}

export function DonationFlowViz({ contributors = [], parasites = 0, healthGrade = 'B' }: DonationFlowVizProps) {
  const [flowOffset, setFlowOffset] = useState(0)
  
  useEffect(() => {
    const interval = setInterval(() => {
      setFlowOffset(prev => (prev + 2) % 100)
    }, 30)
    return () => clearInterval(interval)
  }, [])

  const topContributors = contributors.slice(0, 5)
  const gradeColors: Record<string, string> = {
    'A+': '#00ff00', 'A': '#32cd32', 'B+': '#7cfc00', 'B': '#ffd700',
    'C+': '#ffa500', 'C': '#ff8c00', 'D': '#ff4500', 'F': '#ff0000'
  }

  return (
    <div className="donation-flow-viz">
      <svg viewBox="0 0 300 180" className="w-full h-44">
        <defs>
          <linearGradient id="flowGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#9b30ff" />
            <stop offset="50%" stopColor="#ff69b4" />
            <stop offset="100%" stopColor="#ffd700" />
          </linearGradient>
          <filter id="gemGlow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        
        <g transform="translate(150, 90)" filter="url(#gemGlow)">
          <polygon 
            points="0,-30 26,-15 26,15 0,30 -26,15 -26,-15" 
            fill="url(#flowGradient)"
            stroke="#ffd700"
            strokeWidth="2"
          />
          <text y="5" textAnchor="middle" fill="#fff" fontSize="16" fontWeight="bold">💎</text>
        </g>
        
        {topContributors.map((contributor, index) => {
          const startX = 30
          const startY = 30 + index * 30
          const endX = 124
          const endY = 90
          
          const t = ((flowOffset + index * 20) % 100) / 100
          const particleX = startX + (endX - startX) * t
          const particleY = startY + (endY - startY) * t
          
          return (
            <g key={`flow-${index}`}>
              <path
                d={`M ${startX} ${startY} Q ${80} ${startY + 20} ${endX} ${endY}`}
                fill="none"
                stroke="#9b30ff"
                strokeWidth="2"
                opacity={0.4 + (contributor.donations_given || 100) / 500}
                strokeDasharray="8,4"
              />
              
              <circle
                cx={particleX}
                cy={particleY + Math.sin(t * Math.PI) * -20}
                r="4"
                fill="#ff69b4"
                filter="url(#gemGlow)"
              />
              
              <text x="5" y={startY + 4} fill="#ffeeba" fontSize="8">
                {contributor.player_name?.substring(0, 10) || `Player ${index + 1}`}
              </text>
            </g>
          )
        })}
        
        <g transform="translate(250, 30)">
          <circle cx="0" cy="0" r="25" fill="rgba(0,0,0,0.6)" stroke={gradeColors[healthGrade] || '#ffd700'} strokeWidth="3" />
          <text y="8" textAnchor="middle" fill={gradeColors[healthGrade] || '#ffd700'} fontSize="24" fontWeight="bold">
            {healthGrade}
          </text>
        </g>
        
        {parasites > 0 && (
          <g transform="translate(250, 140)">
            <rect x="-35" y="-15" width="70" height="30" rx="5" fill="rgba(139,0,0,0.6)" stroke="#ff4500" />
            <text y="5" textAnchor="middle" fill="#ff6b6b" fontSize="10" fontWeight="bold">
              🦠 {parasites} parasites
            </text>
          </g>
        )}
      </svg>
    </div>
  )
}

// ==========================================
// Capital Investment Chart
// ==========================================
interface CapitalInvestmentVizProps {
  freeRiders?: number
  inequality?: string
  raidsAnalyzed?: number
}

export function CapitalInvestmentViz({ freeRiders = 0, inequality = 'moderate', raidsAnalyzed = 0 }: CapitalInvestmentVizProps) {
  const [barHeights, setBarHeights] = useState([0, 0, 0, 0, 0])
  
  useEffect(() => {
    const targetHeights = [85, 65, 50, 35, 20]
    const timer = setTimeout(() => {
      setBarHeights(targetHeights)
    }, 100)
    return () => clearTimeout(timer)
  }, [])

  const inequalityColors: Record<string, string> = {
    'low': '#00ff00',
    'moderate': '#ffd700',
    'high': '#ff8c00',
    'extreme': '#ff0000'
  }

  return (
    <div className="capital-investment-viz">
      <svg viewBox="0 0 300 160" className="w-full h-40">
        <defs>
          <linearGradient id="barGradient" x1="0%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" stopColor="#654321" />
            <stop offset="100%" stopColor="#ffd700" />
          </linearGradient>
        </defs>
        
        {[0, 25, 50, 75, 100].map((y, i) => (
          <g key={`grid-${i}`}>
            <line x1="50" y1={130 - y} x2="250" y2={130 - y} stroke="#654321" strokeWidth="0.5" opacity="0.3" />
            <text x="45" y={134 - y} textAnchor="end" fill="#8b6914" fontSize="8">{y}%</text>
          </g>
        ))}
        
        {barHeights.map((height, index) => {
          const x = 70 + index * 40
          return (
            <g key={`bar-${index}`}>
              <rect
                x={x}
                y={130 - height}
                width="25"
                height={height}
                fill="url(#barGradient)"
                stroke="#8b6914"
                strokeWidth="1"
                rx="2"
                style={{
                  transition: 'all 1s ease-out',
                  transitionDelay: `${index * 0.1}s`
                }}
              />
              <text x={x + 12.5} y={125 - height} textAnchor="middle" fontSize="12">🏰</text>
            </g>
          )
        })}
        
        <g transform="translate(150, 15)">
          <text textAnchor="middle" fill="#ffd700" fontSize="10" fontWeight="bold">
            {raidsAnalyzed} RAIDS ANALYZED
          </text>
        </g>
        
        <g transform="translate(260, 60)">
          <rect x="-30" y="-25" width="60" height="50" rx="5" fill="rgba(0,0,0,0.5)" stroke="#8b6914" />
          <text y="-8" textAnchor="middle" fill="#ff8c00" fontSize="8">FREE RIDERS</text>
          <text y="12" textAnchor="middle" fill={freeRiders > 3 ? '#ff4500' : '#ffd700'} fontSize="20" fontWeight="bold">
            {freeRiders}
          </text>
        </g>
        
        <g transform="translate(260, 120)">
          <text y="0" textAnchor="middle" fill="#8b6914" fontSize="8">INEQUALITY</text>
          <text y="15" textAnchor="middle" fill={inequalityColors[inequality] || '#ffd700'} fontSize="10" fontWeight="bold" style={{ textTransform: 'uppercase' }}>
            {inequality}
          </text>
        </g>
      </svg>
    </div>
  )
}

// ==========================================
// Fairness Scale Visualization
// ==========================================
interface FairnessScaleVizProps {
  grade?: string
  winRate?: number
  warsAnalyzed?: number
}

export function FairnessScaleViz({ grade = 'B', winRate = 0.5, warsAnalyzed = 0 }: FairnessScaleVizProps) {
  const scaleAngle = (winRate - 0.5) * 30
  const [pulseScale, setPulseScale] = useState(1)
  
  useEffect(() => {
    const pulseInterval = setInterval(() => {
      setPulseScale(prev => prev === 1 ? 1.05 : 1)
    }, 1000)
    return () => clearInterval(pulseInterval)
  }, [])

  const gradeColors: Record<string, string> = {
    'A+': '#00ff00', 'A': '#32cd32', 'B+': '#7cfc00', 'B': '#ffd700',
    'C+': '#ffa500', 'C': '#ff8c00', 'D': '#ff4500', 'F': '#ff0000'
  }

  return (
    <div className="fairness-scale-viz">
      <svg viewBox="0 0 300 160" className="w-full h-40">
        <defs>
          <linearGradient id="scaleGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#4a3728" />
            <stop offset="50%" stopColor="#ffd700" />
            <stop offset="100%" stopColor="#4a3728" />
          </linearGradient>
        </defs>
        
        <g transform="translate(150, 140)">
          <polygon points="0,-10 -30,10 30,10" fill="#654321" stroke="#8b6914" strokeWidth="2" />
          <rect x="-5" y="-50" width="10" height="40" fill="#4a3728" stroke="#8b6914" />
        </g>
        
        <g 
          transform={`translate(150, 90) rotate(${scaleAngle})`}
          style={{ transition: 'transform 1s ease-out' }}
        >
          <rect x="-100" y="-3" width="200" height="6" rx="3" fill="url(#scaleGradient)" stroke="#8b6914" strokeWidth="1" />
          
          <g transform="translate(-80, 0)">
            <line x1="0" y1="3" x2="0" y2="30" stroke="#8b6914" strokeWidth="2" />
            <ellipse cx="0" cy="35" rx="25" ry="8" fill="#4a3728" stroke="#8b6914" strokeWidth="2" />
            <text y="55" textAnchor="middle" fill="#ffeeba" fontSize="8">YOUR CLAN</text>
            <text y="38" textAnchor="middle" fontSize="12">⚔️</text>
          </g>
          
          <g transform="translate(80, 0)">
            <line x1="0" y1="3" x2="0" y2="30" stroke="#8b6914" strokeWidth="2" />
            <ellipse cx="0" cy="35" rx="25" ry="8" fill="#4a3728" stroke="#8b6914" strokeWidth="2" />
            <text y="55" textAnchor="middle" fill="#ffeeba" fontSize="8">OPPONENTS</text>
            <text y="38" textAnchor="middle" fontSize="12">🛡️</text>
          </g>
          
          <circle cx="0" cy="0" r="8" fill="#ffd700" stroke="#8b6914" strokeWidth="2" />
        </g>
        
        <g 
          transform={`translate(150, 25) scale(${pulseScale})`}
          style={{ transition: 'transform 0.5s ease-out' }}
        >
          <circle cx="0" cy="0" r="22" fill="rgba(0,0,0,0.6)" stroke={gradeColors[grade] || '#ffd700'} strokeWidth="3" />
          <text y="8" textAnchor="middle" fill={gradeColors[grade] || '#ffd700'} fontSize="22" fontWeight="bold">
            {grade}
          </text>
        </g>
        
        <g transform="translate(40, 25)">
          <text textAnchor="middle" fill="#8b6914" fontSize="8">WIN RATE</text>
          <text y="15" textAnchor="middle" fill="#ffd700" fontSize="14" fontWeight="bold">
            {(winRate * 100).toFixed(1)}%
          </text>
        </g>
        
        <g transform="translate(260, 25)">
          <text textAnchor="middle" fill="#8b6914" fontSize="8">WARS</text>
          <text y="15" textAnchor="middle" fill="#ffd700" fontSize="14" fontWeight="bold">
            {warsAnalyzed}
          </text>
        </g>
      </svg>
    </div>
  )
}

// ==========================================
// Trophy Volatility Visualization
// ==========================================
interface TrophyDataPoint {
  day: number
  trophies: number
}

interface TrophyVolatilityVizProps {
  dataPoints?: TrophyDataPoint[]
  prediction?: string
}

export function TrophyVolatilityViz({ dataPoints = [], prediction = 'stable' }: TrophyVolatilityVizProps) {
  const [animatedPoints, setAnimatedPoints] = useState<TrophyDataPoint[]>([])
  
  useEffect(() => {
    const sampleData = dataPoints.length > 0 ? dataPoints : 
      Array.from({ length: 20 }, (_, i) => ({
        day: i,
        trophies: 2000 + Math.sin(i * 0.5) * 200 + Math.random() * 100
      }))
    
    sampleData.forEach((point, index) => {
      setTimeout(() => {
        setAnimatedPoints(prev => [...prev.slice(0, index), point])
      }, index * 50)
    })
  }, [dataPoints])

  const maxTrophies = Math.max(...animatedPoints.map(p => p.trophies || 0), 2500)
  const minTrophies = Math.min(...animatedPoints.map(p => p.trophies || 0), 1500)
  const range = maxTrophies - minTrophies || 1

  const getY = (trophies: number) => 130 - ((trophies - minTrophies) / range) * 100
  const getX = (index: number) => 40 + (index / 19) * 220

  const pathD = animatedPoints.length > 1 
    ? `M ${animatedPoints.map((p, i) => `${getX(i)} ${getY(p.trophies)}`).join(' L ')}`
    : ''

  const predictionColors: Record<string, string> = {
    'rising': '#00ff00',
    'stable': '#ffd700',
    'falling': '#ff4500',
    'volatile': '#ff69b4'
  }

  return (
    <div className="trophy-volatility-viz">
      <svg viewBox="0 0 300 160" className="w-full h-40">
        <defs>
          <linearGradient id="trophyGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#ffd700" stopOpacity={0.8} />
            <stop offset="100%" stopColor="#ffd700" stopOpacity={0} />
          </linearGradient>
          <filter id="trophyGlow">
            <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>
        
        <text x="35" y="35" textAnchor="end" fill="#8b6914" fontSize="8">{Math.round(maxTrophies)}</text>
        <text x="35" y="130" textAnchor="end" fill="#8b6914" fontSize="8">{Math.round(minTrophies)}</text>
        
        {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => (
          <line 
            key={`grid-${i}`}
            x1="40" y1={30 + ratio * 100} 
            x2="260" y2={30 + ratio * 100}
            stroke="#654321" strokeWidth="0.5" opacity="0.3"
          />
        ))}
        
        {animatedPoints.length > 1 && (
          <path
            d={`${pathD} L ${getX(animatedPoints.length - 1)} 130 L 40 130 Z`}
            fill="url(#trophyGradient)"
          />
        )}
        
        <path
          d={pathD}
          fill="none"
          stroke="#ffd700"
          strokeWidth="2"
          filter="url(#trophyGlow)"
          style={{ transition: 'all 0.3s ease-out' }}
        />
        
        {animatedPoints.map((point, index) => (
          <circle
            key={`point-${index}`}
            cx={getX(index)}
            cy={getY(point.trophies)}
            r="3"
            fill="#ffd700"
            stroke="#8b6914"
            strokeWidth="1"
          />
        ))}
        
        {animatedPoints.length > 0 && (
          <text 
            x={getX(animatedPoints.length - 1)} 
            y={getY(animatedPoints[animatedPoints.length - 1]?.trophies || 2000) - 10}
            textAnchor="middle"
            fontSize="14"
          >
            🏆
          </text>
        )}
        
        <g transform="translate(260, 20)">
          <rect x="-30" y="-12" width="60" height="24" rx="4" fill="rgba(0,0,0,0.5)" stroke={predictionColors[prediction] || '#ffd700'} />
          <text y="5" textAnchor="middle" fill={predictionColors[prediction] || '#ffd700'} fontSize="9" fontWeight="bold">
            {prediction?.toUpperCase()}
          </text>
        </g>
        
        <text x="150" y="155" textAnchor="middle" fill="#8b6914" fontSize="9">DAYS</text>
      </svg>
    </div>
  )
}

// ==========================================
// Coordination Heatmap
// ==========================================
interface CoordinationHeatmapProps {
  patterns?: any[]
}

export function CoordinationHeatmap({ patterns = [] }: CoordinationHeatmapProps) {
  const [hoveredCell, setHoveredCell] = useState<string | null>(null)
  
  const hours = ['00:00', '06:00', '12:00', '18:00']
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  
  const getData = (day: number, hour: number) => {
    const seed = day * 4 + hour
    return Math.sin(seed) * 0.5 + 0.5
  }

  const getColor = (value: number) => {
    const r = Math.floor(255 * (1 - value))
    const g = Math.floor(215 * value)
    return `rgb(${r}, ${g}, 0)`
  }

  return (
    <div className="coordination-heatmap">
      <svg viewBox="0 0 300 160" className="w-full h-40">
        {days.map((day, i) => (
          <text key={`day-${i}`} x={55 + i * 32} y="20" textAnchor="middle" fill="#8b6914" fontSize="8">
            {day}
          </text>
        ))}
        
        {hours.map((hour, i) => (
          <text key={`hour-${i}`} x="30" y={45 + i * 30} textAnchor="end" fill="#8b6914" fontSize="8">
            {hour}
          </text>
        ))}
        
        {days.map((_, dayIndex) => (
          hours.map((_, hourIndex) => {
            const value = getData(dayIndex, hourIndex)
            const isHovered = hoveredCell === `${dayIndex}-${hourIndex}`
            return (
              <g key={`cell-${dayIndex}-${hourIndex}`}>
                <rect
                  x={40 + dayIndex * 32}
                  y={30 + hourIndex * 30}
                  width="28"
                  height="26"
                  fill={getColor(value)}
                  stroke={isHovered ? '#fff' : '#654321'}
                  strokeWidth={isHovered ? 2 : 1}
                  rx="3"
                  opacity={0.8 + value * 0.2}
                  onMouseEnter={() => setHoveredCell(`${dayIndex}-${hourIndex}`)}
                  onMouseLeave={() => setHoveredCell(null)}
                  style={{ cursor: 'pointer', transition: 'all 0.2s' }}
                />
                {value > 0.7 && (
                  <text 
                    x={54 + dayIndex * 32} 
                    y={47 + hourIndex * 30} 
                    textAnchor="middle" 
                    fill="#000" 
                    fontSize="10"
                  >
                    ⚡
                  </text>
                )}
              </g>
            )
          })
        ))}
        
        <g transform="translate(260, 50)">
          <text x="0" y="-5" fill="#8b6914" fontSize="8">Activity</text>
          <defs>
            <linearGradient id="legendGradient" x1="0%" y1="100%" x2="0%" y2="0%">
              <stop offset="0%" stopColor="rgb(255, 0, 0)" />
              <stop offset="100%" stopColor="rgb(0, 215, 0)" />
            </linearGradient>
          </defs>
          <rect x="0" y="0" width="15" height="60" fill="url(#legendGradient)" stroke="#8b6914" rx="2" />
          <text x="20" y="10" fill="#00ff00" fontSize="7">High</text>
          <text x="20" y="60" fill="#ff4500" fontSize="7">Low</text>
        </g>
      </svg>
    </div>
  )
}

// ==========================================
// Mini Stat Card with Animation
// ==========================================
interface MiniStatVizProps {
  type: 'leadership' | 'donation' | 'capital' | 'fairness'
  value: number
  label: string
  trend?: 'up' | 'down' | 'stable'
}

export function MiniStatViz({ type, value, label, trend = 'stable' }: MiniStatVizProps) {
  const [animatedValue, setAnimatedValue] = useState(0)
  
  useEffect(() => {
    const duration = 1000
    const steps = 30
    const increment = value / steps
    let current = 0
    
    const timer = setInterval(() => {
      current += increment
      if (current >= value) {
        setAnimatedValue(value)
        clearInterval(timer)
      } else {
        setAnimatedValue(current)
      }
    }, duration / steps)
    
    return () => clearInterval(timer)
  }, [value])

  const trendIcons = {
    'up': '📈',
    'down': '📉',
    'stable': '➡️'
  }

  const trendColors = {
    'up': '#00ff00',
    'down': '#ff4500',
    'stable': '#ffd700'
  }

  const typeIcons = {
    'leadership': '👑',
    'donation': '💎',
    'capital': '🏰',
    'fairness': '⚖️'
  }

  return (
    <div className="mini-stat-viz flex items-center gap-3 p-3 bg-black/30 rounded-lg border border-amber-900/50">
      <div className="text-2xl">{typeIcons[type]}</div>
      <div className="flex-1">
        <div className="text-xs text-yellow-200 uppercase">{label}</div>
        <div className="text-xl font-bold text-coc-gold">
          {animatedValue.toFixed(1)}
        </div>
      </div>
      <div style={{ color: trendColors[trend] }}>{trendIcons[trend]}</div>
    </div>
  )
}
