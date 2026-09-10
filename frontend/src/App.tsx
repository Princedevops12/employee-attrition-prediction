import { useState } from 'react'
import PredictionPage from './pages/PredictionPage'
import DashboardPage from './pages/DashboardPage'
import EmployeesPage from './pages/EmployeesPage'
import { Navbar } from './components/Navbar'

type Page = 'prediction' | 'dashboard' | 'employees'

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('prediction')
  const [darkMode, setDarkMode] = useState(false)

  const toggleDarkMode = () => setDarkMode(!darkMode)

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Navbar
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          darkMode={darkMode}
          onToggleDarkMode={toggleDarkMode}
        />

        <main className="container mx-auto px-4 py-8">
          {currentPage === 'prediction' && <PredictionPage />}
          {currentPage === 'dashboard' && <DashboardPage />}
          {currentPage === 'employees' && <EmployeesPage />}
        </main>
      </div>
    </div>
  )
}
