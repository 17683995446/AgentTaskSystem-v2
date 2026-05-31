class DataManager {
    constructor() {
        this.cache = new Map();
        this.listeners = [];
        this.refreshInterval = null;
    }

    generateMockData(type = 'line', days = 7) {
        const data = {
            line: this.generateLineData(days),
            bar: this.generateBarData(days),
            pie: this.generatePieData(),
            scatter: this.generateScatterData(50),
            radar: this.generateRadarData(),
            gauge: this.generateGaugeData(),
            heatmap: this.generateHeatmapData(),
            area: this.generateAreaData(days)
        };
        return data[type] || data.line;
    }

    generateLineData(days) {
        const labels = [];
        const datasets = [];
        const now = new Date();
        
        for (let i = days - 1; i >= 0; i--) {
            const date = new Date(now);
            date.setDate(date.getDate() - i);
            labels.push(date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }));
        }
        
        datasets.push({
            label: '营收 (万元)',
            data: labels.map(() => Math.floor(Math.random() * 50000) + 20000),
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            tension: 0.4,
            fill: false
        });
        
        datasets.push({
            label: '订单量',
            data: labels.map(() => Math.floor(Math.random() * 1000) + 500),
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            tension: 0.4,
            fill: false
        });
        
        return { labels, datasets };
    }

    generateBarData(days) {
        const labels = ['产品A', '产品B', '产品C', '产品D', '产品E'];
        const datasets = [{
            label: '销售额',
            data: labels.map(() => Math.floor(Math.random() * 80000) + 10000),
            backgroundColor: [
                'rgba(102, 126, 234, 0.8)',
                'rgba(16, 185, 129, 0.8)',
                'rgba(245, 158, 11, 0.8)',
                'rgba(239, 68, 68, 0.8)',
                'rgba(139, 92, 246, 0.8)'
            ],
            borderRadius: 8
        }];
        
        return { labels, datasets };
    }

    generatePieData() {
        const labels = ['直接访问', '搜索引擎', '社交媒体', '推荐链接', '广告投放'];
        const data = labels.map(() => Math.floor(Math.random() * 30) + 10);
        const colors = ['#667eea', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
        
        return {
            labels,
            datasets: [{
                data,
                backgroundColor: colors,
                borderWidth: 0,
                hoverOffset: 10
            }]
        };
    }

    generateScatterData(count) {
        const data = [];
        for (let i = 0; i < count; i++) {
            data.push({
                x: Math.random() * 100,
                y: Math.random() * 100,
                r: Math.floor(Math.random() * 15) + 5
            });
        }
        return {
            datasets: [{
                label: '用户分布',
                data,
                backgroundColor: 'rgba(102, 126, 234, 0.6)',
                pointRadius: 8,
                pointHoverRadius: 12
            }]
        };
    }

    generateRadarData() {
        const labels = ['技术能力', '创新能力', '执行效率', '沟通能力', '团队协作', '项目管理'];
        const data = labels.map(() => Math.floor(Math.random() * 40) + 60);
        
        return {
            labels,
            datasets: [{
                label: '当前评分',
                data,
                backgroundColor: 'rgba(102, 126, 234, 0.2)',
                borderColor: '#667eea',
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointHoverRadius: 8
            }, {
                label: '目标评分',
                data: labels.map(() => 90),
                backgroundColor: 'rgba(16, 185, 129, 0.2)',
                borderColor: '#10b981',
                pointBackgroundColor: '#10b981',
                pointBorderColor: '#fff',
                pointHoverRadius: 8
            }]
        };
    }

    generateGaugeData() {
        const value = Math.floor(Math.random() * 40) + 60;
        return { value, max: 100, label: '完成率' };
    }

    generateHeatmapData() {
        const hours = Array.from({ length: 24 }, (_, i) => `${i}:00`);
        const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
        const data = [];
        
        days.forEach(day => {
            hours.forEach(hour => {
                data.push({
                    day,
                    hour,
                    value: Math.floor(Math.random() * 100)
                });
            });
        });
        
        return { days, hours, data };
    }

    generateAreaData(days) {
        const labels = [];
        const now = new Date();
        
        for (let i = days - 1; i >= 0; i--) {
            const date = new Date(now);
            date.setDate(date.getDate() - i);
            labels.push(date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' }));
        }
        
        return {
            labels,
            datasets: [{
                label: '累计用户',
                data: labels.map((_, i) => Math.floor(1000 + i * 50 + Math.random() * 200)),
                borderColor: '#14b8a6',
                backgroundColor: 'rgba(20, 184, 166, 0.2)',
                fill: true,
                tension: 0.4
            }]
        };
    }

    getData(key) {
        return this.cache.get(key);
    }

    setData(key, value) {
        this.cache.set(key, value);
        this.notifyListeners(key, value);
    }

    subscribe(callback) {
        this.listeners.push(callback);
        return () => {
            this.listeners = this.listeners.filter(cb => cb !== callback);
        };
    }

    notifyListeners(key, data) {
        this.listeners.forEach(callback => callback(key, data));
    }

    startAutoRefresh(interval = 30000) {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        this.refreshInterval = setInterval(() => {
            this.refreshAllData();
        }, interval);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }

    refreshAllData() {
        const chartTypes = ['line', 'bar', 'pie', 'scatter', 'radar', 'gauge', 'heatmap', 'area'];
        chartTypes.forEach(type => {
            const data = this.generateMockData(type);
            this.setData(type, data);
        });
    }

    clearCache() {
        this.cache.clear();
    }
}

window.DataManager = DataManager;
