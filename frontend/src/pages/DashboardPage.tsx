import { BarChart3, Users, AlertCircle, TrendingUp } from 'lucide-react'

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Organization-wide attrition analytics and insights
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Total Employees</p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">1,234</p>
            </div>
            <Users className="h-8 w-8 text-primary-500 opacity-20" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">At Risk</p>
              <p className="text-3xl font-bold text-red-600 dark:text-red-400">187</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">15.2% of total</p>
            </div>
            <AlertCircle className="h-8 w-8 text-red-500 opacity-20" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Attrition Rate</p>
              <p className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">16.2%</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">Last 12 months</p>
            </div>
            <TrendingUp className="h-8 w-8 text-yellow-500 opacity-20" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Model Accuracy</p>
              <p className="text-3xl font-bold text-green-600 dark:text-green-400">87.3%</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">F1-Score: 0.83</p>
            </div>
            <BarChart3 className="h-8 w-8 text-green-500 opacity-20" />
          </div>
        </div>
      </div>

      {/* Charts Placeholder */}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="card">
          <h2 className="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Attrition by Department</h2>
          <div className="flex h-64 items-center justify-center rounded-lg bg-gray-100 dark:bg-gray-700">
            <p className="text-gray-500 dark:text-gray-400">Chart visualization coming soon</p>
          </div>
        </div>

        <div className="card">
          <h2 className="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Attrition by Age Group</h2>
          <div className="flex h-64 items-center justify-center rounded-lg bg-gray-100 dark:bg-gray-700">
            <p className="text-gray-500 dark:text-gray-400">Chart visualization coming soon</p>
          </div>
        </div>

        <div className="card">
          <h2 className="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Attrition by Salary Band</h2>
          <div className="flex h-64 items-center justify-center rounded-lg bg-gray-100 dark:bg-gray-700">
            <p className="text-gray-500 dark:text-gray-400">Chart visualization coming soon</p>
          </div>
        </div>

        <div className="card">
          <h2 className="mb-4 text-lg font-semibold text-gray-900 dark:text-white">Top Risk Factors</h2>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Distance from Home</span>
              <span className="font-semibold">High</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Job Satisfaction</span>
              <span className="font-semibold">High</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Work-Life Balance</span>
              <span className="font-semibold">Medium</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Tenure</span>
              <span className="font-semibold">Medium</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
