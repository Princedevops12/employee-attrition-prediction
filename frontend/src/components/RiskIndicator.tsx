import { AlertCircle, CheckCircle, AlertTriangle } from 'lucide-react'

interface RiskIndicatorProps {
  riskLevel: 'Low' | 'Medium' | 'High'
  probability: number
}

export function RiskIndicator({ riskLevel, probability }: RiskIndicatorProps) {
  const getRiskColor = () => {
    switch (riskLevel) {
      case 'Low':
        return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-100'
      case 'Medium':
        return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-100'
      case 'High':
        return 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-100'
    }
  }

  const getRiskIcon = () => {
    switch (riskLevel) {
      case 'Low':
        return <CheckCircle className="h-5 w-5" />
      case 'Medium':
        return <AlertTriangle className="h-5 w-5" />
      case 'High':
        return <AlertCircle className="h-5 w-5" />
    }
  }

  const percentageWidth = Math.round(probability * 100)

  return (
    <div className="space-y-3">
      <div className={`flex items-center gap-2 rounded-lg p-3 ${getRiskColor()}`}>
        {getRiskIcon()}
        <div>
          <p className="font-semibold">{riskLevel} Risk</p>
          <p className="text-sm opacity-80">{Math.round(probability * 100)}% probability of attrition</p>
        </div>
      </div>

      {/* Risk gauge */}
      <div className="space-y-2">
        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Risk Gauge</p>
        <div className="h-3 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
          <div
            className={`h-full transition-all duration-300 ${
              riskLevel === 'Low' ? 'bg-green-500' : riskLevel === 'Medium' ? 'bg-yellow-500' : 'bg-red-500'
            }`}
            style={{ width: `${percentageWidth}%` }}
          />
        </div>
        <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
          <span>0%</span>
          <span>50%</span>
          <span>100%</span>
        </div>
      </div>
    </div>
  )
}
