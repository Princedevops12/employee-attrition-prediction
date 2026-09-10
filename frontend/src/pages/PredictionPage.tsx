import { useState } from 'react'
import { apiService, PredictionRequest, PredictionResponse } from '../services/api'
import { RiskIndicator } from '../components/RiskIndicator'
import { Loader, Send } from 'lucide-react'

export default function PredictionPage() {
  const [formData, setFormData] = useState<PredictionRequest>({
    age: 45,
    monthly_income: 5500,
    years_at_company: 10,
    years_in_current_role: 5,
    years_with_curr_manager: 3,
    total_working_years: 15,
    job_satisfaction: 3,
    work_life_balance: 3,
    job_role: 'Sales Executive',
    department: 'Sales',
    distance_from_home: 5,
    over_time: 'No',
  })

  const [prediction, setPrediction] = useState<PredictionResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: ['age', 'monthly_income', 'years_at_company', 'years_in_current_role',
              'years_with_curr_manager', 'total_working_years', 'job_satisfaction',
              'work_life_balance', 'distance_from_home'].includes(name) ? parseInt(value) : value,
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setPrediction(null)

    try {
      const result = await apiService.predictSingle(formData)
      setPrediction(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get prediction')
    } finally {
      setLoading(false)
    }
  }

  const departments = ['Sales', 'Research & Development', 'Human Resources']
  const jobRoles = ['Sales Executive', 'Research Scientist', 'Laboratory Technician',
                    'Manufacturing Director', 'Healthcare Representative', 'Manager']

  return (
    <div className="space-y-8">
      <div>
        <h1 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white">Attrition Risk Prediction</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Enter employee details to predict attrition risk
        </p>
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        {/* Form */}
        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              {/* Personal Information */}
              <div>
                <label className="label-text">Age</label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  min="18"
                  max="100"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label-text">Gender (Job Satisfaction)</label>
                <input
                  type="number"
                  name="job_satisfaction"
                  value={formData.job_satisfaction}
                  onChange={handleChange}
                  min="1"
                  max="4"
                  className="input-field"
                  required
                />
              </div>

              {/* Financial */}
              <div className="sm:col-span-2">
                <label className="label-text">Monthly Income ($)</label>
                <input
                  type="number"
                  name="monthly_income"
                  value={formData.monthly_income}
                  onChange={handleChange}
                  min="0"
                  step="100"
                  className="input-field"
                  required
                />
              </div>

              {/* Tenure */}
              <div>
                <label className="label-text">Years at Company</label>
                <input
                  type="number"
                  name="years_at_company"
                  value={formData.years_at_company}
                  onChange={handleChange}
                  min="0"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label-text">Years in Current Role</label>
                <input
                  type="number"
                  name="years_in_current_role"
                  value={formData.years_in_current_role}
                  onChange={handleChange}
                  min="0"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label-text">Years with Manager</label>
                <input
                  type="number"
                  name="years_with_curr_manager"
                  value={formData.years_with_curr_manager}
                  onChange={handleChange}
                  min="0"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label-text">Total Working Years</label>
                <input
                  type="number"
                  name="total_working_years"
                  value={formData.total_working_years}
                  onChange={handleChange}
                  min="0"
                  className="input-field"
                  required
                />
              </div>

              {/* Satisfaction */}
              <div>
                <label className="label-text">Work-Life Balance (1-4)</label>
                <input
                  type="number"
                  name="work_life_balance"
                  value={formData.work_life_balance}
                  onChange={handleChange}
                  min="1"
                  max="4"
                  className="input-field"
                  required
                />
              </div>

              {/* Work Info */}
              <div className="sm:col-span-2">
                <label className="label-text">Department</label>
                <select name="department" value={formData.department} onChange={handleChange} className="input-field" required>
                  {departments.map(dept => (
                    <option key={dept} value={dept}>
                      {dept}
                    </option>
                  ))}
                </select>
              </div>

              <div className="sm:col-span-2">
                <label className="label-text">Job Role</label>
                <select name="job_role" value={formData.job_role} onChange={handleChange} className="input-field" required>
                  {jobRoles.map(role => (
                    <option key={role} value={role}>
                      {role}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="label-text">Distance from Home (km)</label>
                <input
                  type="number"
                  name="distance_from_home"
                  value={formData.distance_from_home}
                  onChange={handleChange}
                  min="0"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="label-text">Overtime</label>
                <select name="over_time" value={formData.over_time} onChange={handleChange} className="input-field" required>
                  <option value="Yes">Yes</option>
                  <option value="No">No</option>
                </select>
              </div>
            </div>

            {error && <div className="rounded-lg bg-red-50 p-4 text-red-800 dark:bg-red-900 dark:text-red-100">{error}</div>}

            <button type="submit" disabled={loading} className="btn-primary w-full">
              {loading ? (
                <>
                  <Loader className="h-4 w-4 animate-spin" />
                  Predicting...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
                  Get Prediction
                </>
              )}
            </button>
          </form>
        </div>

        {/* Results */}
        <div>
          {prediction ? (
            <div className="card">
              <h2 className="mb-6 text-xl font-bold text-gray-900 dark:text-white">Prediction Results</h2>
              <RiskIndicator riskLevel={prediction.risk_level} probability={prediction.probability} />

              <div className="mt-6 space-y-4 border-t border-gray-200 pt-6 dark:border-gray-700">
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Probability</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{(prediction.probability * 100).toFixed(1)}%</p>
                </div>
                <div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Model Confidence</p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">{(prediction.confidence * 100).toFixed(1)}%</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="card">
              <p className="text-center text-gray-500 dark:text-gray-400">Fill in the form and click "Get Prediction" to see results</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
