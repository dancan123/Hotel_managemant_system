/**
 * Chart Service Module
 * Handles all chart generation and visualization
 */

class ChartService {
    static charts = {};

    /**
     * Destroy existing chart
     */
    static destroyChart(chartId) {
        if (ChartService.charts[chartId]) {
            ChartService.charts[chartId].destroy();
            delete ChartService.charts[chartId];
        }
    }

    /**
     * Draw sales trend chart
     */
    static drawSalesTrendChart(trendData) {
        ChartService.destroyChart('salesTrendChart');

        const ctx = document.getElementById('salesTrendChart').getContext('2d');
        const labels = trendData.map(item => new Date(item.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        const data = trendData.map(item => item.total_sales);

        ChartService.charts['salesTrendChart'] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Daily Sales',
                    data: data,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#3498db',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Draw category breakdown chart
     */
    static drawCategoryChart(categoryData) {
        ChartService.destroyChart('categoryBreakdownChart');

        const ctx = document.getElementById('categoryBreakdownChart').getContext('2d');
        const labels = categoryData.map(item => item.category);
        const data = categoryData.map(item => item.total);

        const colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6'];

        ChartService.charts['categoryBreakdownChart'] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors.slice(0, labels.length),
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }

    /**
     * Draw monthly sales chart
     */
    static drawMonthlySalesChart(monthlyData) {
        ChartService.destroyChart('monthlySalesChart');

        const ctx = document.getElementById('monthlySalesChart');
        if (!ctx) return;

        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        const data = Array(12).fill(0);

        monthlyData.forEach(item => {
            data[item.month - 1] = item.total;
        });

        ChartService.charts['monthlySalesChart'] = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: months,
                datasets: [{
                    label: 'Monthly Sales',
                    data: data,
                    backgroundColor: '#3498db',
                    borderColor: '#2980b9',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Draw employee performance chart
     */
    static drawEmployeePerformanceChart(employeeData) {
        ChartService.destroyChart('employeePerformanceChart');

        const ctx = document.getElementById('employeePerformanceChart');
        if (!ctx) return;

        const labels = employeeData.map(item => item.employee_name);
        const data = employeeData.map(item => item.total_sales);

        ChartService.charts['employeePerformanceChart'] = new Chart(ctx.getContext('2d'), {
            type: 'horizontalBar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Total Sales',
                    data: data,
                    backgroundColor: '#2ecc71',
                    borderColor: '#27ae60',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                indexAxis: 'y',
                scales: {
                    x: {
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
    }

    /**
     * Draw occupancy chart
     */
    static drawOccupancyChart(occupancyData) {
        ChartService.destroyChart('occupancyChart');

        const ctx = document.getElementById('occupancyChart');
        if (!ctx) return;

        ChartService.charts['occupancyChart'] = new Chart(ctx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: ['Occupied', 'Available', 'Maintenance'],
                datasets: [{
                    data: [
                        occupancyData.occupied_rooms,
                        occupancyData.available_rooms,
                        occupancyData.maintenance_rooms
                    ],
                    backgroundColor: ['#e74c3c', '#2ecc71', '#f39c12'],
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    /**
     * Draw payment method chart
     */
    static drawPaymentMethodChart(paymentData) {
        ChartService.destroyChart('paymentMethodChart');

        const ctx = document.getElementById('paymentMethodChart');
        if (!ctx) return;

        const labels = paymentData.map(item => item.payment_method || 'Unknown');
        const data = paymentData.map(item => item.count);

        ChartService.charts['paymentMethodChart'] = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Transactions',
                    data: data,
                    backgroundColor: '#9b59b6',
                    borderColor: '#8e44ad',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}
