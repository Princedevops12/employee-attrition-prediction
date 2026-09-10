import { Moon, Sun, TrendingUp, Users, Zap } from 'lucide-react'

type Page = 'prediction' | 'dashboard' | 'employees'

interface NavbarProps {
  currentPage: Page
  onPageChange: (page: Page) => void
  darkMode: boolean
  onToggleDarkMode: () => void
}

export function Navbar({ currentPage, onPageChange, darkMode, onToggleDarkMode }: NavbarProps) {
  const isActive = (page: Page) => currentPage === page

  return (
    <nav className="border-b border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-800">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between py-4">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-6 w-6 text-primary-500" />
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">AttritionPred</h1>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={() => onPageChange('prediction')}
              className={`flex items-center gap-2 rounded-lg px-4 py-2 transition-colors ${
                isActive('prediction')
                  ? 'bg-primary-500 text-white'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
              }`}
            >
              <Zap className="h-4 w-4" />
              Predict
            </button>

            <button
              onClick={() => onPageChange('dashboard')}
              className={`flex items-center gap-2 rounded-lg px-4 py-2 transition-colors ${
                isActive('dashboard')
                  ? 'bg-primary-500 text-white'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
              }`}
            >
              <TrendingUp className="h-4 w-4" />
              Dashboard
            </button>

            <button
              onClick={() => onPageChange('employees')}
              className={`flex items-center gap-2 rounded-lg px-4 py-2 transition-colors ${
                isActive('employees')
                  ? 'bg-primary-500 text-white'
                  : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
              }`}
            >
              <Users className="h-4 w-4" />
              Employees
            </button>
          </div>

          <button
            onClick={onToggleDarkMode}
            className="rounded-lg p-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
            aria-label="Toggle dark mode"
          >
            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>
        </div>
      </div>
    </nav>
  )
}
