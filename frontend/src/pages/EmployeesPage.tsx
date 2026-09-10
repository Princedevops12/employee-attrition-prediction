import { useState, useEffect } from "react";
import { apiService, Employee } from "../services/api";
import { Search, Plus, Trash2, Loader } from "lucide-react";

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("");
  const [showForm, setShowForm] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    department: "Sales",
    job_role: "Sales Executive",
    age: 30,
    gender: "Male",
    monthly_income: 5000,
    years_at_company: 1,
    job_satisfaction: 3,
    work_life_balance: 3,
  });

  useEffect(() => {
    loadEmployees();
  }, [departmentFilter]);

  const loadEmployees = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.listEmployees(
        0,
        50,
        departmentFilter || undefined,
      );
      setEmployees(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load employees");
    } finally {
      setLoading(false);
    }
  };

  const handleAddEmployee = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiService.createEmployee(formData);
      setShowForm(false);
      setFormData({
        name: "",
        department: "Sales",
        job_role: "Sales Executive",
        age: 30,
        gender: "Male",
        monthly_income: 5000,
        years_at_company: 1,
        job_satisfaction: 3,
        work_life_balance: 3,
      });
      loadEmployees();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to add employee");
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm("Are you sure you want to delete this employee?")) {
      try {
        await apiService.deleteEmployee(id);
        loadEmployees();
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to delete employee",
        );
      }
    }
  };

  const filteredEmployees = employees.filter(
    (emp) =>
      emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      emp.job_role.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white">
            Employees
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage employee records and view attrition predictions
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          Add Employee
        </button>
      </div>

      {/* Add Employee Form */}
      {showForm && (
        <div className="card">
          <h2 className="mb-4 text-lg font-semibold text-gray-900 dark:text-white">
            Add New Employee
          </h2>
          <form onSubmit={handleAddEmployee} className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <input
                type="text"
                placeholder="Full Name"
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                className="input-field"
                required
              />
              <select
                value={formData.department}
                onChange={(e) =>
                  setFormData({ ...formData, department: e.target.value })
                }
                className="input-field"
              >
                <option value="Sales">Sales</option>
                <option value="Research & Development">
                  Research & Development
                </option>
                <option value="Human Resources">Human Resources</option>
              </select>
              <input
                type="text"
                placeholder="Job Role"
                value={formData.job_role}
                onChange={(e) =>
                  setFormData({ ...formData, job_role: e.target.value })
                }
                className="input-field"
              />
              <input
                type="number"
                placeholder="Age"
                value={formData.age}
                onChange={(e) =>
                  setFormData({ ...formData, age: parseInt(e.target.value) })
                }
                className="input-field"
                min="18"
              />
              <input
                type="number"
                placeholder="Monthly Income"
                value={formData.monthly_income}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    monthly_income: parseFloat(e.target.value),
                  })
                }
                className="input-field"
                min="0"
              />
              <input
                type="number"
                placeholder="Years at Company"
                value={formData.years_at_company}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    years_at_company: parseInt(e.target.value),
                  })
                }
                className="input-field"
                min="0"
              />
            </div>
            <div className="flex gap-2">
              <button type="submit" className="btn-primary">
                Save Employee
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Search and Filter */}
      <div className="card space-y-4">
        <div className="flex gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search by name or role..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>
          <select
            value={departmentFilter}
            onChange={(e) => setDepartmentFilter(e.target.value)}
            className="input-field w-48"
          >
            <option value="">All Departments</option>
            <option value="Sales">Sales</option>
            <option value="Research & Development">
              Research & Development
            </option>
            <option value="Human Resources">Human Resources</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="rounded-lg bg-red-50 p-4 text-red-800 dark:bg-red-900 dark:text-red-100">
          {error}
        </div>
      )}

      {/* Employees Table */}
      {loading ? (
        <div className="flex items-center justify-center py-12">
          <Loader className="h-8 w-8 animate-spin text-primary-500" />
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Name
                </th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Department
                </th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Job Role
                </th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Age
                </th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Income
                </th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Tenure
                </th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-900 dark:text-white">
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredEmployees.map((emp) => (
                <tr
                  key={emp.id}
                  className="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"
                >
                  <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                    {emp.name}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                    {emp.department}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                    {emp.job_role}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                    {emp.age}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                    ${emp.monthly_income.toLocaleString()}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                    {emp.years_at_company} yrs
                  </td>
                  <td className="px-4 py-3 text-sm">
                    <button
                      onClick={() => handleDelete(emp.id)}
                      className="text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-300"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {filteredEmployees.length === 0 && (
            <div className="flex items-center justify-center py-12">
              <p className="text-gray-500 dark:text-gray-400">
                No employees found
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
