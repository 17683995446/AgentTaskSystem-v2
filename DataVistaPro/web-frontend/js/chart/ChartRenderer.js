class ChartRenderer {
    constructor() {
        this.charts = {};
        this.colors = {
            primary: '#667eea',
            secondary: '#10b981',
            warning: '#f59e0b',
            danger: '#ef4444',
            purple: '#8b5cf6',
            cyan: '#06b6d4',
            teal: '#14b8a6',
            pink: '#ec4899'
        };
    }

    renderLineChart(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: data,
            options: this.getLineOptions()
        });
    }

    renderBarChart(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: data,
            options: this.getBarOptions()
        });
    }

    renderPieChart(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'pie',
            data: data,
            options: this.getPieOptions()
        });
    }

    renderScatterChart(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'scatter',
            data: data,
            options: this.getScatterOptions()
        });
    }

    renderRadarChart(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'radar',
            data: data,
            options: this.getRadarOptions()
        });
    }

    renderGaugeChart(canvasId, data) {
        const container = document.getElementById(canvasId).parentElement;
        const gaugeDiv = document.createElement('div');
        gaugeDiv.className = 'gauge-container';
        gaugeDiv.innerHTML = `
            <div class="gauge-value">
                <div class="number">${data.value}%</div>
                <div class="label">${data.label}</div>
            </div>
        `;
        
        const canvas = document.getElementById(canvasId);
        canvas.style.display = 'none';
        
        if (container.querySelector('.gauge-container')) {
            container.querySelector('.gauge-container').remove();
        }
        container.appendChild(gaugeDiv);
        
        const gaugeChart = echarts.init(container);
        const option = this.getGaugeOption(data);
        gaugeChart.setOption(option);
        
        this.charts[canvasId] = gaugeChart;
    }

    renderHeatmapChart(canvasId, data) {
        const container = document.getElementById(canvasId).parentElement;
        const heatmapDiv = document.createElement('div');
        heatmapDiv.style.width = '100%';
        heatmapDiv.style.height = '250px';
        
        const canvas = document.getElementById(canvasId);
        canvas.style.display = 'none';
        
        if (container.querySelector('div[style*="height: 250px"]')) {
            container.querySelector('div[style*="height: 250px"]').remove();
        }
        container.appendChild(heatmapDiv);
        
        const heatmapChart = echarts.init(heatmapDiv);
        const option = this.getHeatmapOption(data);
        heatmapChart.setOption(option);
        
        this.charts[canvasId] = heatmapChart;
    }

    renderAreaChart(canvasId, data) {
        const ctx = document.getElementById(canvasId).getContext('2d');
        
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
        }
        
        this.charts[canvasId] = new Chart(ctx, {
            type: 'line',
            data: data,
            options: this.getAreaOptions()
        });
    }

    renderChart(canvasId, type, data) {
        switch (type) {
            case 'line':
                this.renderLineChart(canvasId, data);
                break;
            case 'bar':
                this.renderBarChart(canvasId, data);
                break;
            case 'pie':
                this.renderPieChart(canvasId, data);
                break;
            case 'scatter':
                this.renderScatterChart(canvasId, data);
                break;
            case 'radar':
                this.renderRadarChart(canvasId, data);
                break;
            case 'gauge':
                this.renderGaugeChart(canvasId, data);
                break;
            case 'heatmap':
                this.renderHeatmapChart(canvasId, data);
                break;
            case 'area':
                this.renderAreaChart(canvasId, data);
                break;
        }
    }

    updateChart(canvasId, newData) {
        if (this.charts[canvasId]) {
            const chart = this.charts[canvasId];
            if (chart.data) {
                chart.data = newData;
                chart.update();
            }
        }
    }

    destroyChart(canvasId) {
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }
    }

    getBaseOptions() {
        return {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: getComputedStyle(document.body).getPropertyValue('--text-primary'),
                        padding: 15,
                        usePointStyle: true,
                        font: { size: 12 }
                    }
                },
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    padding: 12,
                    cornerRadius: 8
                }
            }
        };
    }

    getLineOptions() {
        return {
            ...this.getBaseOptions(),
            scales: {
                x: {
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { color: getComputedStyle(document.body).getPropertyValue('--text-secondary') }
                },
                y: {
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { color: getComputedStyle(document.body).getPropertyValue('--text-secondary') }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeOutQuart'
            }
        };
    }

    getBarOptions() {
        return {
            ...this.getBaseOptions(),
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: getComputedStyle(document.body).getPropertyValue('--text-secondary') }
                },
                y: {
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { color: getComputedStyle(document.body).getPropertyValue('--text-secondary') }
                }
            },
            animation: {
                duration: 1000,
                easing: 'easeOutBounce'
            }
        };
    }

    getPieOptions() {
        return {
            ...this.getBaseOptions(),
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: getComputedStyle(document.body).getPropertyValue('--text-primary'),
                        padding: 15,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.raw / total) * 100).toFixed(1);
                            return `${context.label}: ${context.raw} (${percentage}%)`;
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                animateScale: true
            }
        };
    }

    getScatterOptions() {
        return {
            ...this.getBaseOptions(),
            scales: {
                x: {
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { color: getComputedStyle(document.body).getPropertyValue('--text-secondary') },
                    title: { display: true, text: 'X轴', color: getComputedStyle(document.body).getPropertyValue('--text-secondary') }
                },
                y: {
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { color: getComputedStyle(document.body).getPropertyValue('--text-secondary') },
                    title: { display: true, text: 'Y轴', color: getComputedStyle(document.body).getPropertyValue('--text-secondary') }
                }
            }
        };
    }

    getRadarOptions() {
        return {
            ...this.getBaseOptions(),
            scales: {
                r: {
                    angleLines: { color: 'rgba(0, 0, 0, 0.1)' },
                    grid: { color: 'rgba(0, 0, 0, 0.1)' },
                    pointLabels: {
                        color: getComputedStyle(document.body).getPropertyValue('--text-primary'),
                        font: { size: 11 }
                    }
                }
            },
            animation: {
                duration: 1500
            }
        };
    }

    getGaugeOption(data) {
        return {
            series: [{
                type: 'gauge',
                startAngle: 180,
                endAngle: 0,
                min: 0,
                max: data.max,
                splitNumber: 10,
                itemStyle: {
                    color: '#667eea'
                },
                progress: {
                    show: true,
                    width: 18
                },
                pointer: {
                    show: false
                },
                axisLine: {
                    lineStyle: {
                        width: 18,
                        color: [[1, '#e5e7eb']]
                    }
                },
                axisTick: { show: false },
                splitLine: { show: false },
                axisLabel: { show: false },
                anchor: { show: false },
                title: { show: false },
                detail: { show: false }
            }]
        };
    }

    getHeatmapOption(data) {
        const hours = data.hours;
        const days = data.days;
        const chartData = data.data.map(d => [
            hours.indexOf(d.hour),
            days.indexOf(d.day),
            d.value
        ]);
        
        return {
            tooltip: {
                position: 'top'
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: hours,
                splitArea: { show: true }
            },
            yAxis: {
                type: 'category',
                data: days,
                splitArea: { show: true }
            },
            visualMap: {
                min: 0,
                max: 100,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '0%',
                inRange: {
                    color: ['#e0f2fe', '#7dd3fc', '#0ea5e9', '#0369a1', '#0c4a6e']
                }
            },
            series: [{
                name: '活跃度',
                type: 'heatmap',
                data: chartData,
                label: { show: false },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
    }

    getAreaOptions() {
        return {
            ...this.getLineOptions(),
            fill: true,
            backgroundColor: 'rgba(20, 184, 166, 0.1)',
            interaction: {
                intersect: false,
                mode: 'index'
            }
        };
    }
}

window.ChartRenderer = ChartRenderer;
