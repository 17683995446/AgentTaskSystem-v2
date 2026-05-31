document.addEventListener('DOMContentLoaded', function() {
    console.log('DataVista Pro - Initializing...');
    
    const dataManager = new DataManager();
    const chartRenderer = new ChartRenderer();
    const dashboardController = new DashboardController(dataManager, chartRenderer);
    
    dashboardController.loadTheme();
    
    console.log('DataVista Pro - Initialization complete');
    
    setTimeout(() => {
        dashboardController.showNotification('欢迎使用 DataVista Pro', 'success');
    }, 1000);
    
    window.DataVistaApp = {
        dataManager,
        chartRenderer,
        dashboardController,
        
        refresh: () => dashboardController.refreshAllCharts(),
        toggleTheme: () => dashboardController.toggleTheme(),
        switchIndicator: (id) => dashboardController.switchIndicator(id),
        switchChartType: (type) => dashboardController.switchChartType(type),
        openTaskManager: () => window.open('task-manager.html', '_blank')
    };
    
    const taskManagerBtn = document.getElementById('taskManagerBtn');
    if (taskManagerBtn) {
        taskManagerBtn.addEventListener('click', () => {
            window.open('task-manager.html', '_blank');
        });
    }
});
