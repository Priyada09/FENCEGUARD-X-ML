# Dashboard README

## Overview
FENCEGUARD-X dashboard provides real-time visualization of fence status, event logging, and analytics. Built with React, Vite, and WebSocket.

## Quick Start

### Prerequisites
- Node.js 18+
- npm or yarn
- Backend running on http://localhost:5000

### Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Opens http://localhost:5173 (Vite default port)
```

## Dashboard Structure

```
dashboard/
├─ src/
│  ├─ components/
│  │  ├─ FenceStatus.jsx         # Live status indicator
│  │  ├─ EventLog.jsx            # Event history table
│  │  ├─ Analytics.jsx           # Charts & graphs
│  │  ├─ AlertPanel.jsx          # Alert notifications
│  │  └─ Navbar.jsx              # Navigation header
│  │
│  ├─ pages/
│  │  ├─ Dashboard.jsx           # Main dashboard view
│  │  ├─ Analytics.jsx           # Detailed analytics
│  │  ├─ Settings.jsx            # Configuration
│  │  └─ NotFound.jsx            # 404 page
│  │
│  ├─ redux/
│  │  ├─ slices/
│  │  │  ├─ fenceSlice.js        # Fence state
│  │  │  ├─ eventsSlice.js       # Events state
│  │  │  └─ uiSlice.js           # UI state
│  │  └─ store.js                # Redux store config
│  │
│  ├─ services/
│  │  ├─ api.js                  # Axios instance
│  │  ├─ websocket.js            # Socket.io connection
│  │  └─ auth.js                 # JWT token management
│  │
│  ├─ styles/
│  │  └─ tailwind.css            # Tailwind configuration
│  │
│  ├─ App.jsx                    # Root component
│  └─ main.jsx                   # Entry point
│
├─ public/                        # Static assets
├─ index.html                     # HTML template
├─ tailwind.config.js             # Tailwind config
├─ vite.config.js                 # Vite config
├─ package.json
└─ README.md
```

## Key Components

### 1. Fence Status (FenceStatus.jsx)
```jsx
// Real-time fence status with color-coded indicators
// GREEN:  Normal operation
// YELLOW: Alert (threshold exceeded)
// RED:    Critical (relay cut)

// Displays:
├─ Current: 1.23A (with limit)
├─ Voltage: 380V (with min/max)
├─ Temperature: 28.5°C
├─ Uptime: 99.8%
└─ Last Update: 5 seconds ago
```

### 2. Event Log (EventLog.jsx)
```jsx
// Searchable table of all fence events
Columns:
├─ Timestamp
├─ Event Type (Normal/Alert/Critical)
├─ Current (A)
├─ Voltage (V)
├─ Action Taken
└─ Details

Features:
├─ Pagination (20 per page)
├─ Search/Filter by event type
├─ Sort by timestamp
└─ Export to CSV
```

### 3. Analytics (Analytics.jsx)
```jsx
// Charts showing historical trends
├─ Current vs Time (line chart)
├─ Voltage vs Time (line chart)
├─ Event frequency (bar chart)
├─ Uptime percentage (gauge)
└─ Response time distribution (histogram)

Time Ranges:
├─ Last 24 hours
├─ Last 7 days
├─ Last 30 days
└─ Custom range
```

### 4. Alert Panel (AlertPanel.jsx)
```jsx
// Toast notifications for critical events
├─ Critical event: RED banner
├─ Alert event: YELLOW banner
├─ Recovery: GREEN banner
└─ Auto-dismiss after 5 seconds
```

## State Management (Redux)

### Fence Slice (fenceSlice.js)
```javascript
{
  status: 'normal',        // 'normal' | 'alert' | 'critical'
  current: 1.23,           // Amperes
  voltage: 380,            // Volts
  temperature: 28.5,       // Celsius
  uptime: 0.998,           // Percentage
  lastUpdate: Date,
  relayState: 'on'         // 'on' | 'off'
}
```

### Events Slice (eventsSlice.js)
```javascript
{
  events: [
    {
      _id: "...",
      sensorId: "ESP32-001",
      eventType: "alert",
      current: 2.87,
      voltage: 375,
      timestamp: Date,
      action: "notify"
    },
    // ... more events
  ],
  filter: 'all',           // 'all' | 'critical' | 'alert'
  page: 1,
  total: 145
}
```

## API Integration

### Axios Instance (api.js)
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api/v1',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
});

// Automatically add JWT to all requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### WebSocket Connection (websocket.js)
```javascript
import io from 'socket.io-client';

const socket = io('http://localhost:5000', {
  auth: {
    token: localStorage.getItem('token')
  }
});

// Listen for real-time events
socket.on('event:new', (event) => {
  dispatch(addEvent(event));
  dispatch(showAlert(event));
});

socket.on('status:update', (status) => {
  dispatch(updateStatus(status));
});
```

## Features

### Real-Time Updates
- WebSocket connection (Socket.io) for instant updates
- Dashboard refreshes without page reload
- Alert notifications on critical events

### Search & Filter
- Search events by sensor ID
- Filter by event type (Normal/Alert/Critical)
- Date range filtering
- Pagination

### Export Data
```javascript
// Export events to CSV
exportToCSV(events) {
  // Converts events array to CSV format
  // Downloads as "events_export.csv"
}
```

### Responsive Design
- Mobile-friendly layout (Tailwind CSS)
- Collapsible sidebar navigation
- Touch-friendly buttons and controls

### Dark Mode (Optional)
```javascript
// Toggle dark/light theme
const [isDark, setIsDark] = useState(false);
// Tailwind dark: prefix handles styling
```

## Styling with Tailwind CSS

### Color Scheme
```css
/* Status Colors */
--success: #10B981 (Green)   /* Normal */
--warning: #F59E0B (Yellow)  /* Alert */
--danger:  #EF4444 (Red)     /* Critical */
--info:    #3B82F6 (Blue)    /* Information */
```

### Responsive Breakpoints
```
sm: 640px   (mobile)
md: 768px   (tablet)
lg: 1024px  (desktop)
xl: 1280px  (wide)
```

## Build & Deployment

### Development
```bash
npm run dev          # Start dev server with hot reload
```

### Production Build
```bash
npm run build        # Build optimized bundle
npm run preview      # Preview production build locally
```

### Deployment Options

#### Vercel (Recommended)
```bash
npm install -g vercel
vercel              # Deploy to Vercel
vercel --prod       # Production deployment
```

#### Netlify
```bash
npm run build
# Connect repo to Netlify, auto-deploys on push
```

#### Static Hosting (GitHub Pages)
```bash
npm run build
# Upload dist/ folder to GitHub Pages
```

## Environment Configuration

Create `.env.local`:
```env
VITE_API_URL=http://localhost:5000/api/v1
VITE_WS_URL=http://localhost:5000
VITE_LOG_LEVEL=debug
```

## Testing

### Unit Tests (Vitest)
```bash
npm run test        # Run all tests
npm run test:watch  # Watch mode
npm run test:ui     # UI for test results
```

### Component Tests (React Testing Library)
```bash
# Example: FenceStatus component
test('displays current status in green', () => {
  render(<FenceStatus status="normal" current={1.23} />);
  expect(screen.getByText('NORMAL')).toHaveClass('text-green-500');
});
```

### E2E Tests (Cypress)
```bash
npm run cypress:open  # Open Cypress test runner
npm run cypress:run   # Run all E2E tests
```

## Performance Optimization

### Code Splitting
```javascript
// Lazy load analytics page
const Analytics = React.lazy(() => import('./pages/Analytics'));

// Suspense boundary
<Suspense fallback={<Loading />}>
  <Analytics />
</Suspense>
```

### Memoization
```javascript
// Prevent unnecessary re-renders
const EventLog = React.memo(({ events, filter }) => {
  // Component only re-renders if props change
});
```

### Image Optimization
```javascript
// Use lazy loading for images
<img loading="lazy" src="..." alt="..." />
```

## Accessibility (a11y)

- ARIA labels for interactive elements
- Keyboard navigation support
- Color contrast >4.5:1
- Screen reader friendly

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Dashboard won't connect | Check backend running on :5000, verify CORS |
| Events not updating | Check WebSocket connection, verify JWT token |
| Charts not rendering | Ensure data is fetched, check browser console |
| Styling looks off | Clear browser cache, rebuild with `npm run build` |

## Next Steps

1. [Setup Backend](../backend/README.md)
2. [Configure Firmware](../firmware/README.md)
3. [Run Full Integration](../integration-tests/)

---

**Contact**: Ananya (Presentation Lead)
**Last Updated**: 14 August 2026
