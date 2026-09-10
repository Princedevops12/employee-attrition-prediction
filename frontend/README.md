# Frontend - Employee Attrition Prediction UI

Modern React 18 frontend built with TypeScript, Vite, and Tailwind CSS for the Employee Attrition Prediction system.

## Features

- **Prediction Page**: Interactive form to predict employee attrition risk with visual risk indicators
- **Dashboard**: Organization-wide analytics with attrition metrics by department, age, salary
- **Employee Management**: CRUD operations for employee records with search and filtering
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop
- **Dark Mode**: Dark/light mode toggle with system preference detection
- **Real-time API Integration**: Connects to FastAPI backend for predictions and data management
- **Type Safety**: Full TypeScript implementation with proper type checking

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client for API requests
- **Lucide React** - Icon library
- **Recharts** - Charts and visualizations (ready for integration)

## Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── PredictionPage.tsx     # Main prediction form
│   │   ├── DashboardPage.tsx      # Analytics dashboard
│   │   └── EmployeesPage.tsx      # Employee management
│   ├── components/
│   │   ├── Navbar.tsx             # Navigation bar
│   │   └── RiskIndicator.tsx      # Risk visualization
│   ├── services/
│   │   └── api.ts                 # API client and service
│   ├── App.tsx                    # Main app component
│   ├── main.tsx                   # Entry point
│   └── index.css                  # Global styles (Tailwind)
├── public/                         # Static assets
├── index.html                      # HTML entry point
├── vite.config.ts                 # Vite configuration
├── tsconfig.json                  # TypeScript configuration
├── tailwind.config.ts             # Tailwind CSS configuration
├── postcss.config.js              # PostCSS configuration
└── package.json                   # Dependencies
```

## Setup

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Navigate to frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local to set API base URL
   ```

### Development

Start the development server:

```bash
npm run dev
```

The app will run at `http://localhost:5173`

### Build

Create a production build:

```bash
npm run build
```

The build output is in the `dist/` directory.

### Preview

Preview the production build locally:

```bash
npm run preview
```

## API Integration

The frontend communicates with the FastAPI backend via the `apiService` module in `src/services/api.ts`.

### Available API Endpoints

- `POST /api/predict` - Single employee attrition prediction
- `POST /api/predict/batch` - Batch CSV predictions
- `GET /api/model/metrics` - Model performance metrics
- `GET /api/employees` - List employees
- `POST /api/employees` - Create employee
- `GET /api/employees/{id}` - Get employee details
- `PUT /api/employees/{id}` - Update employee
- `DELETE /api/employees/{id}` - Delete employee
- `GET /api/employees/department/{dept}/stats` - Department statistics

### Environment Variables

- `VITE_API_BASE_URL` - Base URL for API (default: `http://localhost:8000`)

## Pages

### Prediction Page

Interactive form for entering employee details and getting attrition predictions.

**Features:**

- 12-field form for employee information
- Real-time form validation
- Visual risk indicator with probability gauge
- Risk level classification (Low/Medium/High)
- Model confidence score

### Dashboard Page

Organization-wide analytics and insights.

**Metrics:**

- Total employees count
- Number at risk with percentage
- Overall attrition rate
- Model accuracy

**Visualizations (Ready for integration):**

- Attrition by department
- Attrition by age group
- Attrition by salary band
- Top risk factors

### Employees Page

Employee records management.

**Features:**

- Add new employee records
- View all employees with pagination
- Search by name or job role
- Filter by department
- Delete employee records
- Responsive table layout

## Component Architecture

### Navbar

Navigation component with:

- Page switcher (Prediction, Dashboard, Employees)
- Dark/light mode toggle
- Branding

### RiskIndicator

Visual component for displaying:

- Risk level badge (Low/Medium/High with color coding)
- Probability percentage
- Risk gauge with progressive indicator

### API Service

Centralized API client with:

- Type-safe request/response models
- Error handling
- Health check endpoint
- Batch operations

## Styling

### Tailwind CSS

The project uses Tailwind CSS for styling with:

- Custom color palette (primary: sky blue)
- Dark mode support
- Utility classes
- Custom component classes (`.card`, `.btn-primary`, `.input-field`, etc.)

### Custom Utilities

- `.card` - Styled container/panel
- `.btn-primary` - Primary action button
- `.btn-secondary` - Secondary action button
- `.input-field` - Consistent form input styling
- `.label-text` - Form label styling

## Dark Mode

Dark mode is toggled via the sun/moon icon in the navbar. The preference is stored in component state and applies to all components via the `.dark` class on the root HTML element.

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Performance Optimizations

- Code splitting with Vite
- Lazy component loading ready
- Image optimization ready
- API request caching ready

## Testing

Run linting:

```bash
npm run lint
```

Type checking:

```bash
npm run type-check
```

## Deployment

See [DEPLOY.md](../DEPLOY.md) in the root directory for Render deployment instructions.

### Build Output

```bash
npm run build
```

The `dist/` directory contains the static files ready for deployment:

- Minified JavaScript
- Optimized CSS
- Bundled assets

### Render Static Site

Deploy as a static site on Render:

1. Push code to GitHub
2. Create new Static Site on Render
3. Set Build Command: `cd frontend && npm install && npm run build`
4. Set Publish Directory: `frontend/dist`
5. Set environment variable: `VITE_API_BASE_URL=<your-api-url>`

## Future Enhancements

- [ ] Integrate Recharts for dashboard visualizations
- [ ] Add employee profile pages
- [ ] Implement CSV export for predictions
- [ ] Add real-time notifications
- [ ] Implement user authentication
- [ ] Add data refresh/sync indicators
- [ ] Performance monitoring
- [ ] Analytics tracking
