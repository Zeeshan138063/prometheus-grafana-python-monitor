# Prometheus Grafana Python Monitor 🔍

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Prometheus](https://img.shields.io/badge/prometheus-latest-orange.svg)
![Grafana](https://img.shields.io/badge/grafana-latest-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A production-ready monitoring solution for Python applications using Prometheus and Grafana. This project provides real-time metrics collection, custom dashboards, and comprehensive monitoring for web scrapers and Python applications.

## 📋 Features

- Real-time metrics monitoring
- Custom Prometheus metrics for Python applications
- Pre-configured Grafana dashboards
- Sample web scraper implementation
- Comprehensive monitoring setup guide
- Best practices documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Linux/macOS/Windows

### Installation

1. **Install Python Dependencies**
```bash
pip install prometheus_client requests beautifulsoup4
```

2. **Install Prometheus**
- Visit [Prometheus Downloads](https://prometheus.io/download/) for the latest version
- Download and extract Prometheus
- Go inside of prometheus folder

3. **Install Grafana**
- Visit [Grafana Downloads](https://grafana.com/grafana/download) for the latest version
- Follow installation instructions for your OS

## ⚙️ Configuration

### Prometheus Setup

1. **Inside of promethus folder update prometheus.yml**
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'scraper_metrics'
    static_configs:
      - targets: ['localhost:8000']
```

2. **Start Prometheus**
```bash
./prometheus --config.file=prometheus.yml
```

### Grafana Setup

1. **Start Grafana**
```bash
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

2. **Access Grafana**
- URL: `http://localhost:3000`
- Default credentials: `admin`/`admin`

3. **Configure Data Source**
- Navigate to: Configuration (⚙️) → Data Sources
- Add Prometheus data source
- Set URL to your Prometheus instance
- Click "Save & Test"

## 📊 Command Reference

### Prometheus Commands

| Operation | Command | Description |
|-----------|---------|-------------|
| Start | `./prometheus --config.file=prometheus.yml` | Start with config |
| Custom Port | `./prometheus --web.listen-address=:9091` | Use different port |
| Health Check | `curl localhost:9090/-/healthy` | Check status |
| Reload Config | `curl -X POST localhost:9090/-/reload` | Reload config |

### Grafana Commands

| Operation | Command | Description |
|-----------|---------|-------------|
| Start | `sudo systemctl start grafana-server` | Start service |
| Enable | `sudo systemctl enable grafana-server` | Enable on boot |
| Status | `sudo systemctl status grafana-server` | Check status |
| Restart | `sudo systemctl restart grafana-server` | Restart service |

## 💻 Sample Implementation

```python
from prometheus_client import start_http_server, Counter, Gauge, Summary
import requests
from bs4 import BeautifulSoup
import time
import random

# Define Prometheus metrics
SCRAPES_TOTAL = Counter('scraper_pages_scraped_total', 'Total number of pages scraped')
SCRAPE_ERRORS = Counter('scraper_errors_total', 'Total number of scraping errors')
SCRAPE_DURATION = Summary('scraper_scrape_duration_seconds', 'Time spent scraping pages')
ACTIVE_SCRAPERS = Gauge('scraper_active_scrapers', 'Number of active scrapers')

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
    
    def scrape_page(self, url):
        try:
            ACTIVE_SCRAPERS.inc()
            with SCRAPE_DURATION.time():
                response = self.session.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                time.sleep(random.uniform(0.5, 2))
            SCRAPES_TOTAL.inc()
            return True
        except Exception as e:
            SCRAPE_ERRORS.inc()
            print(f"Error scraping {url}: {str(e)}")
            return False
        finally:
            ACTIVE_SCRAPERS.dec()

def main():
    start_http_server(8000)
    print("Prometheus metrics server started on port 8000")
    scraper = WebScraper()
    urls = ["http://example.com", "http://example.org", "http://example.net"]
    while True:
        for url in urls:
            scraper.scrape_page(url)
        time.sleep(60)

if __name__ == "__main__":
    main()
```

## 📈 Metrics & Dashboards

### Available Metrics
- `scraper_pages_scraped_total`: Counter of scraped pages
- `scraper_errors_total`: Counter of scraping errors
- `scraper_scrape_duration_seconds`: Summary of scraping duration
- `scraper_active_scrapers`: Gauge of active scrapers

### Dashboard Queries

1. **Success Rate**
```promql
rate(scraper_pages_scraped_total[5m])
```

2. **Error Rate**
```promql
rate(scraper_errors_total[5m])
```

3. **Active Scrapers**
```promql
scraper_active_scrapers
```

## 🔧 Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Check port usage: `sudo lsof -i :9090`
   - Use alternative port
   - Update configurations accordingly

2. **Connection Issues**
   - Verify services are running
   - Check firewall settings
   - Validate configurations

## 📚 Documentation

- [Prometheus Documentation](https://prometheus.io/docs/introduction/overview/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Project Wiki](./docs/BEST_PRACTICES.md)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✨ Acknowledgments

- Prometheus team for their monitoring solution
- Grafana Labs for their visualization platform
- Python community for prometheus_client library

## 📫 Support

- [Open an Issue](https://github.com/username/prometheus-grafana-python-monitor/issues)
- [Project Discussions](https://github.com/username/prometheus-grafana-python-monitor/discussions)
