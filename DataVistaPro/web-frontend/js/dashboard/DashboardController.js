class DashboardController {
    constructor(dataManager, chartRenderer) {
        this.dataManager = dataManager;
        this.chartRenderer = chartRenderer;
        this.currentIndicator = 'revenue';
        this.currentChartType = 'line';
        this.isAnimating = false;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadAllCharts();
        this.startAutoRefresh();
    }

    bindEvents() {
        document.querySelectorAll('.indicator-item').forEach(item => {
            item.addEventListener('click', (e) => {
                this.switchIndicator(e.target.dataset.id);
            });
        });

        document.querySelectorAll('.chart-type-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const btn = e.target.closest('.chart-type-btn');
                this.switchChartType(btn.dataset.type);
            });
        });

        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshAllCharts();
        });

        document.getElementById('themeToggle').addEventListener('click', () => {
            this.toggleTheme();
        });

        document.getElementById('timeRange').addEventListener('change', (e) => {
            this.changeTimeRange(e.target.value);
        });

        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    loadAllCharts() {
        const chartConfigs = [
            { id: 'lineChart', type: 'line' },
            { id: 'barChart', type: 'bar' },
            { id: 'pieChart', type: 'pie' },
            { id: 'scatterChart', type: 'scatter' },
            { id: 'radarChart', type: 'radar' },
            { id: 'gaugeChart', type: 'gauge' },
            { id: 'heatmapChart', type: 'heatmap' },
            { id: 'areaChart', type: 'area' }
        ];

        chartConfigs.forEach(config => {
            this.loadChart(config.id, config.type);
        });
    }

    loadChart(canvasId, type) {
        const days = this.getDaysFromTimeRange();
        const data = this.dataManager.generateMockData(type, days);
        this.dataManager.setData(canvasId, data);
        this.chartRenderer.renderChart(canvasId, type, data);
    }

    refreshAllCharts() {
        if (this.isAnimating) return;
        
        this.isAnimating = true;
        const chartIds = ['lineChart', 'barChart', 'pieChart', 'scatterChart', 'radarChart', 'gaugeChart', 'heatmapChart', 'areaChart'];
        
        chartIds.forEach((canvasId, index) => {
            setTimeout(() => {
                const type = canvasId.replace('Chart', '').toLowerCase();
                if (type === 'gauge') {
                    const data = this.dataManager.generateMockData(type);
                    this.chartRenderer.renderChart(canvasId, type, data);
                } else if (type === 'heatmap') {
                    const data = this.dataManager.generateMockData(type);
                    this.chartRenderer.renderChart(canvasId, type, data);
                } else {
                    const data = this.dataManager.generateMockData(type);
                    this.chartRenderer.renderChart(canvasId, type, data);
                }
            }, index * 100);
        });

        setTimeout(() => {
            this.isAnimating = false;
            this.showNotification('数据已刷新', 'success');
        }, chartIds.length * 100 + 500);
    }

    switchIndicator(indicatorId) {
        document.querySelectorAll('.indicator-item').forEach(item => {
            item.classList.remove('active');
        });
        
        const activeItem = document.querySelector(`.indicator-item[data-id="${indicatorId}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
        
        this.currentIndicator = indicatorId;
        this.refreshAllCharts();
    }

    switchChartType(type) {
        document.querySelectorAll('.chart-type-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        const activeBtn = document.querySelector(`.chart-type-btn[data-type="${type}"]`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }
        
        this.currentChartType = type;
        
        const firstChartCard = document.querySelector('.chart-card');
        if (firstChartCard) {
            const canvas = firstChartCard.querySelector('canvas');
            if (canvas) {
                const canvasId = canvas.id;
                this.loadChart(canvasId, type);
            }
        }
    }

    toggleTheme() {
        const body = document.body;
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        setTimeout(() => {
            this.refreshAllCharts();
        }, 100);
    }

    loadTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme);
    }

    changeTimeRange(range) {
        const daysMap = {
            '24h': 1,
            '7d': 7,
            '30d': 30,
            '90d': 90
        };
        const days = daysMap[range] || 7;
        this.refreshAllCharts();
    }

    getDaysFromTimeRange() {
        const range = document.getElementById('timeRange').value;
        const daysMap = {
            '24h': 1,
            '7d': 7,
            '30d': 30,
            '90d': 90
        };
        return daysMap[range] || 7;
    }

    startAutoRefresh() {
        this.dataManager.startAutoRefresh(60000);
        this.dataManager.subscribe((key, data) => {
            if (key.endsWith('Chart')) {
                const type = key.replace('Chart', '').toLowerCase();
                if (type === 'gauge') {
                    this.chartRenderer.renderChart(key, type, data);
                } else if (type === 'heatmap') {
                    this.chartRenderer.renderChart(key, type, data);
                } else {
                    this.chartRenderer.updateChart(key, data);
                }
            }
        });
    }

    stopAutoRefresh() {
        this.dataManager.stopAutoRefresh();
    }

    handleResize() {
        clearTimeout(this.resizeTimeout);
        this.resizeTimeout = setTimeout(() => {
            Object.keys(this.chartRenderer.charts).forEach(canvasId => {
                const chart = this.chartRenderer.charts[canvasId];
                if (chart && chart.resize) {
                    chart.resize();
                }
            });
        }, 250);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: var(--bg-card);
            border-left: 4px solid ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#667eea'};
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            animation: slideInRight 0.3s ease-out;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }
}

window.DashboardController = DashboardController;
