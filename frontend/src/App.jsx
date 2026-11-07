
import { useEffect, useState } from "react";
import axios from "axios";
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer
} from "recharts";
import {
  LayoutDashboard, TrendingUp, Package, Globe2,
  CalendarDays, Activity, RefreshCw
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:8000";

const money = (value) =>
  new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
    maximumFractionDigits: 0
  }).format(value || 0);

const compactMoney = (value) =>
  `£${(value / 1000).toFixed(0)}k`;

function App() {
  const [overview, setOverview] = useState(null);
  const [monthly, setMonthly] = useState([]);
  const [products, setProducts] = useState([]);
  const [countries, setCountries] = useState([]);
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboard = async () => {
    setLoading(true);
    setError("");

    try {
      const [o, m, p, c, f] = await Promise.all([
        axios.get(`${API}/api/overview`),
        axios.get(`${API}/api/monthly-sales`),
        axios.get(`${API}/api/top-products`),
        axios.get(`${API}/api/top-countries`),
        axios.get(`${API}/api/forecast`)
      ]);

      setOverview(o.data);
      setMonthly(m.data);
      setProducts(p.data);
      setCountries(c.data);
      setForecast(f.data);
    } catch (err) {
      console.error(err);
      setError("Unable to load dashboard data. Check that the FastAPI backend is running.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const forecastRows = forecast.map((item) => {
    const dateKey = Object.keys(item).find(
      (key) => key.toLowerCase().includes("date")
    );
    const valueKey = Object.keys(item).find(
      (key) =>
        key.toLowerCase().includes("predicted") ||
        key.toLowerCase().includes("forecast")
    );

    return {
      date: dateKey ? String(item[dateKey]).slice(0, 10) : "",
      sales: valueKey ? Number(item[valueKey]) : 0
    };
  });

  const forecastTotal = forecastRows.reduce((sum, item) => sum + item.sales, 0);
  const forecastAverage = forecastRows.length
    ? forecastTotal / forecastRows.length
    : 0;

  const navItems = [
    { icon: LayoutDashboard, label: "Overview", href: "#overview" },
    { icon: TrendingUp, label: "Sales Analytics", href: "#sales" },
    { icon: Package, label: "Products", href: "#products" },
    { icon: Globe2, label: "Markets", href: "#markets" },
    { icon: CalendarDays, label: "Forecast", href: "#forecast" }
  ];

  if (loading) {
    return <div className="loading-screen">Loading Sales Intelligence...</div>;
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">S</div>
          <div>
            <h2>Sales<span>Pulse</span></h2>
            <p>INTELLIGENCE PLATFORM</p>
          </div>
        </div>

        <div className="nav-heading">WORKSPACE</div>
        <nav>
          {navItems.map((item, index) => {
            const Icon = item.icon;
            return (
              <a
                href={item.href}
                key={item.label}
                className={`nav-link ${index === 0 ? "active" : ""}`}
              >
                <Icon size={18} />
                <span>{item.label}</span>
              </a>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="status-dot"></div>
          <div>
            <strong>System operational</strong>
            <p>Sales API connected</p>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">BUSINESS INTELLIGENCE / OVERVIEW</p>
            <h1>Sales Overview<span>.</span></h1>
          </div>
          <button className="refresh-button" onClick={loadDashboard}>
            <RefreshCw size={16} /> Refresh data
          </button>
        </header>

        {error && <div className="error-banner">{error}</div>}

        <section className="welcome-row" id="overview">
          <div>
            <h2>Good insights start here.</h2>
            <p>Explore performance, discover patterns and forecast what's next.</p>
          </div>
          <div className="dataset-tag">
            <span></span> ONLINE RETAIL II · 2009–2011
          </div>
        </section>

        <section className="kpi-grid">
          <div className="kpi-card coral-card">
            <div className="kpi-top">
              <span>Total Revenue</span>
              <TrendingUp size={19} />
            </div>
            <h2>{money(overview?.total_revenue)}</h2>
            <p>Across all cleaned transactions</p>
          </div>

          <div className="kpi-card">
            <div className="kpi-top">
              <span>Total Orders</span>
              <Activity size={19} />
            </div>
            <h2>{(overview?.total_orders || 0).toLocaleString("en-GB")}</h2>
            <p>Unique invoice transactions</p>
          </div>

          <div className="kpi-card">
            <div className="kpi-top">
              <span>Units Sold</span>
              <Package size={19} />
            </div>
            <h2>{(overview?.total_units || 0).toLocaleString("en-GB")}</h2>
            <p>Total quantity purchased</p>
          </div>

          <div className="kpi-card lime-card">
            <div className="kpi-top">
              <span>Forecast Horizon</span>
              <CalendarDays size={19} />
            </div>
            <h2>{forecast.length} days</h2>
            <p>Forward-looking sales projection</p>
          </div>
        </section>

        <section className="chart-grid" id="sales">
          <div className="panel revenue-panel">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">PERFORMANCE</p>
                <h3>Monthly revenue</h3>
              </div>
              <span className="panel-chip">HISTORICAL</span>
            </div>

            <div className="chart-area">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={monthly}>
                  <defs>
                    <linearGradient id="revenueFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#FF784F" stopOpacity={0.35} />
                      <stop offset="95%" stopColor="#FF784F" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid stroke="#303030" vertical={false} />
                  <XAxis dataKey="InvoiceDate" stroke="#888" tick={{ fill: "#999", fontSize: 11 }} tickLine={false} axisLine={false} />
                  <YAxis tickFormatter={compactMoney} stroke="#888" tick={{ fill: "#999", fontSize: 11 }} tickLine={false} axisLine={false} />
                  <Tooltip
                    contentStyle={{ background: "#222", border: "1px solid #444", borderRadius: 10 }}
                    formatter={(value) => money(value)}
                  />
                  <Area type="monotone" dataKey="Revenue" stroke="#FF784F" strokeWidth={3} fill="url(#revenueFill)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="panel forecast-summary" id="forecast">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">PREDICTIVE ANALYTICS</p>
                <h3>30-day outlook</h3>
              </div>
              <span className="live-chip">MODEL OUTPUT</span>
            </div>
            <div className="forecast-total">{money(forecastTotal)}</div>
            <p className="muted">Total projected revenue across the forecast period</p>
            <div className="forecast-divider"></div>
            <div className="forecast-stats">
              <div>
                <span>Daily average</span>
                <strong>{money(forecastAverage)}</strong>
              </div>
              <div>
                <span>Forecast days</span>
                <strong>{forecast.length}</strong>
              </div>
            </div>
            <div className="forecast-note">
              <TrendingUp size={17} />
              <span>Forecast generated using your trained Random Forest model.</span>
            </div>
          </div>
        </section>

        <section className="chart-grid lower-grid">
          <div className="panel" id="products">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">PRODUCT PERFORMANCE</p>
                <h3>Top 10 products</h3>
              </div>
              <Package size={19} className="heading-icon" />
            </div>
            <div className="chart-area product-chart">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={products} layout="vertical" margin={{ left: 15, right: 15 }}>
                  <CartesianGrid stroke="#303030" horizontal={false} />
                  <XAxis type="number" tickFormatter={compactMoney} stroke="#888" tick={{ fill: "#999", fontSize: 10 }} />
                  <YAxis
                    type="category"
                    dataKey="Description"
                    width={135}
                    stroke="#888"
                    tick={{ fill: "#ccc", fontSize: 10 }}
                    tickFormatter={(value) => value.length > 20 ? value.slice(0, 20) + "…" : value}
                  />
                  <Tooltip
                    contentStyle={{ background: "#222", border: "1px solid #444", borderRadius: 10 }}
                    formatter={(value) => money(value)}
                  />
                  <Bar dataKey="Revenue" fill="#C5F36A" radius={[0, 5, 5, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="panel" id="markets">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">GEOGRAPHIC PERFORMANCE</p>
                <h3>Top markets</h3>
              </div>
              <Globe2 size={19} className="heading-icon" />
            </div>
            <div className="market-list">
              {countries.map((country, index) => {
                const max = countries[0]?.Revenue || 1;
                return (
                  <div className="market-item" key={country.Country}>
                    <div className="market-info">
                      <span className="market-rank">{String(index + 1).padStart(2, "0")}</span>
                      <strong>{country.Country}</strong>
                      <span>{money(country.Revenue)}</span>
                    </div>
                    <div className="market-track">
                      <div
                        className="market-fill"
                        style={{ width: `${(country.Revenue / max) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        <section className="panel forecast-chart-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">FUTURE PERFORMANCE</p>
              <h3>30-day sales forecast</h3>
            </div>
            <span className="panel-chip violet-chip">RANDOM FOREST</span>
          </div>
          <div className="chart-area">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={forecastRows}>
                <defs>
                  <linearGradient id="forecastFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#A78BFA" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#A78BFA" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="#303030" vertical={false} />
                <XAxis dataKey="date" stroke="#888" tick={{ fill: "#999", fontSize: 10 }} tickLine={false} axisLine={false} minTickGap={25} />
                <YAxis tickFormatter={compactMoney} stroke="#888" tick={{ fill: "#999", fontSize: 11 }} tickLine={false} axisLine={false} />
                <Tooltip
                  contentStyle={{ background: "#222", border: "1px solid #444", borderRadius: 10 }}
                  formatter={(value) => money(value)}
                />
                <Area type="monotone" dataKey="sales" stroke="#A78BFA" strokeWidth={3} fill="url(#forecastFill)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <p className="chart-footnote">
            Historical demonstration forecast: these dates continue from the 2009–2011 dataset,
            not a prediction of current real-world sales.
          </p>
        </section>

        <footer className="footer">
          <span>SALES PULSE <b>·</b> BUSINESS INTELLIGENCE</span>
          <span>Built with React · FastAPI · Python · Recharts</span>
        </footer>
      </main>
    </div>
  );
}

export default App;
