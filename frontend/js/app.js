/**
 * Main Application Controller
 * Handles page navigation and core functionality
 */

let currentUser = null;
let currentPage = 'dashboard';

/**
 * Initialize the application
 */
async function initApp() {
    console.log('Initializing app...');
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initApp);
        return;
    }
    
    // Check if user is already logged in
    const token = APIService.getToken();
    
    if (token) {
        try {
            const response = await APIService.getProfile();
            if (response.success) {
                currentUser = response.user;
                showMainDashboard();
                initializeDashboard();
            }
        } catch (error) {
            console.error('Session expired:', error);
            APIService.clearToken();
            showLoginPage();
        }
    } else {
        showLoginPage();
    }
}

/**
 * Show login page
 */
function showLoginPage() {
    console.log('Showing login page');
    const loginPage = document.getElementById('loginPage');
    const mainDash = document.getElementById('mainDashboard');
    
    if (loginPage) loginPage.style.display = 'block';
    if (mainDash) mainDash.style.display = 'none';
    
    setupLoginForm();
}

/**
 * Show main dashboard
 */
function showMainDashboard() {
    console.log('Showing main dashboard');
    const loginPage = document.getElementById('loginPage');
    const mainDash = document.getElementById('mainDashboard');
    
    if (loginPage) loginPage.style.display = 'none';
    if (mainDash) mainDash.style.display = 'block';
    
    updateUserDisplay();
    setupPageVisibility();
}

/**
 * Setup login form handler
 */
function setupLoginForm() {
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');

    if (!loginForm) {
        console.error('Login form not found!');
        return;
    }

    // Remove any previous listeners by cloning
    const newForm = loginForm.cloneNode(true);
    loginForm.parentNode.replaceChild(newForm, loginForm);
    
    const updatedForm = document.getElementById('loginForm');
    const updatedError = document.getElementById('loginError');
    
    updatedForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Login form submitted');

        const usernameInput = document.getElementById('username');
        const passwordInput = document.getElementById('password');
        
        if (!usernameInput || !passwordInput) {
            console.error('Form inputs not found');
            return;
        }

        const username = usernameInput.value.trim();
        const password = passwordInput.value;

        if (!username || !password) {
            updatedError.textContent = 'Please enter username and password.';
            updatedError.style.display = 'block';
            return;
        }

        try {
            console.log('Attempting login with username:', username);
            const response = await APIService.login(username, password);
            console.log('Login response:', response);

            if (response && response.success && response.token) {
                APIService.setToken(response.token);
                currentUser = response.user;
                console.log('Login successful, user:', currentUser);
                showMainDashboard();
                initializeDashboard();
            } else {
                updatedError.textContent = 'Invalid credentials. Please try again.';
                updatedError.style.display = 'block';
            }
        } catch (error) {
            console.error('Login error:', error);
            updatedError.textContent = 'Invalid credentials or server error. Please try again.';
            updatedError.style.display = 'block';
            setTimeout(() => {
                updatedError.style.display = 'none';
            }, 3000);
        }
    });

    // Setup logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
}

/**
 * Update user display information
 */
function updateUserDisplay() {
    if (currentUser) {
        const currentUserEl = document.getElementById('currentUser');
        if (currentUserEl) {
            currentUserEl.textContent = `${currentUser.full_name} (${currentUser.role})`;
        }
    }

    // Setup role-based visibility
    const role = currentUser?.role;

    // Show/hide role-specific elements
    const navEmployees = document.getElementById('navEmployees');
    const navReports = document.getElementById('navReports');
    const adminOnlyAddEmployee = document.getElementById('adminOnlyAddEmployee');
    const adminOnlyCheckIn = document.getElementById('adminOnlyCheckIn');

    if (role === 'Employee') {
        if (navEmployees) navEmployees.style.display = 'none';
        if (navReports) navReports.style.display = 'none';
        if (adminOnlyAddEmployee) adminOnlyAddEmployee.style.display = 'none';
        if (adminOnlyCheckIn) adminOnlyCheckIn.style.display = 'none';
    } else if (role === 'Manager') {
        if (navEmployees) navEmployees.style.display = 'inline-block';
        if (navReports) navReports.style.display = 'inline-block';
        if (adminOnlyAddEmployee) adminOnlyAddEmployee.style.display = 'none';
        if (adminOnlyCheckIn) adminOnlyCheckIn.style.display = 'inline-block';
    } else if (role === 'Admin') {
        if (navEmployees) navEmployees.style.display = 'inline-block';
        if (navReports) navReports.style.display = 'inline-block';
        if (adminOnlyAddEmployee) adminOnlyAddEmployee.style.display = 'inline-block';
        if (adminOnlyCheckIn) adminOnlyCheckIn.style.display = 'inline-block';
    }
}

/**
 * Setup page visibility based on role
 */
function setupPageVisibility() {
    // Set up nav links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('data-page');
            if (page) {
                showPage(page);
            }
        });
    });
}

/**
 * Show a specific page
 */
function showPage(page) {
    // Hide all pages
    document.querySelectorAll('.page-content').forEach(element => {
        element.style.display = 'none';
    });

    // Show selected page
    const pageElement = document.getElementById(page);
    if (pageElement) {
        pageElement.style.display = 'block';

        // Update nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            if (link.getAttribute('data-page') === page) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        currentPage = page;

        // Initialize page-specific content
        if (page === 'dashboard') {
            initializeDashboard();
        } else if (page === 'sales') {
            initializeSalesPage();
        } else if (page === 'rooms') {
            initializeRoomsPage();
        } else if (page === 'employees') {
            initializeEmployeesPage();
        } else if (page === 'reports') {
            initializeReportsPage();
        }
    }
}

/**
 * Initialize dashboard
 */
async function initializeDashboard() {
    try {
        console.log('Initializing dashboard');
        
        // Update current date
        const today = new Date().toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
        const currentDateEl = document.getElementById('currentDate');
        if (currentDateEl) {
            currentDateEl.textContent = today;
        }

        // Get dashboard data
        const overview = await APIService.getDashboardOverview();
        console.log('Dashboard overview:', overview);
        
        if (overview && overview.overview) {
            const todaySalesEl = document.getElementById('todaySales');
            const totalTransEl = document.getElementById('totalTransactions');
            const occupancyEl = document.getElementById('occupancyRate');
            const occupiedEl = document.getElementById('occupiedRooms');
            const totalRoomsEl = document.getElementById('totalRoomsText');

            if (todaySalesEl) todaySalesEl.textContent = `$${overview.overview.today_sales.toFixed(2)}`;
            if (totalTransEl) totalTransEl.textContent = overview.overview.total_transactions;
            if (occupancyEl) occupancyEl.textContent = `${overview.overview.occupancy_rate.toFixed(1)}%`;
            if (occupiedEl) occupiedEl.textContent = overview.overview.occupied_rooms;
            if (totalRoomsEl) totalRoomsEl.textContent = `of ${overview.overview.total_rooms} rooms`;
        }

        // Get sales trend
        const trend = await APIService.getSalesTrend(7);
        if (trend && trend.trend) {
            ChartService.drawSalesTrendChart(trend.trend);
        }

        // Get category breakdown
        const todayStr = new Date().toISOString().split('T')[0];
        const categories = await APIService.getCategoryBreakdown(todayStr);
        if (categories && categories.breakdown) {
            ChartService.drawCategoryChart(categories.breakdown);
        }

        // Get employee leaderboard
        const leaderboard = await APIService.getEmployeeLeaderboard(30);
        if (leaderboard && leaderboard.leaderboard) {
            updateTopPerformers(leaderboard.leaderboard);
        }

        // Set today's date as default
        const saleDateEl = document.getElementById('saleDate');
        const reportDateEl = document.getElementById('reportDate');
        if (saleDateEl) saleDateEl.valueAsDate = new Date();
        if (reportDateEl) reportDateEl.valueAsDate = new Date();

    } catch (error) {
        console.error('Error initializing dashboard:', error);
    }
}

/**
 * Update top performers table
 */
function updateTopPerformers(performers) {
    const tbody = document.getElementById('topPerformersTable');
    if (!tbody) return;
    
    tbody.innerHTML = '';

    if (!performers || performers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; padding: 20px;">No performance data available</td></tr>';
        return;
    }

    performers.slice(0, 10).forEach((performer, index) => {
        const row = tbody.insertRow();
        const avg = performer.transactions > 0 ? performer.total / performer.transactions : 0;
        row.innerHTML = `
            <td>${index + 1}. ${performer.name}</td>
            <td>$${performer.total.toFixed(2)}</td>
            <td>${performer.transactions}</td>
            <td>$${avg.toFixed(2)}</td>
        `;
    });
}

/**
 * Initialize sales page
 */
async function initializeSalesPage() {
    try {
        console.log('Initializing sales page');
        const today = new Date().toISOString().split('T')[0];
        const response = await APIService.getDailySales(currentUser.user_id, today);

        const tbody = document.getElementById('salesTable');
        if (!tbody) return;
        
        tbody.innerHTML = '';

        if (response && response.sales && response.sales.length > 0) {
            response.sales.forEach(sale => {
                const row = tbody.insertRow();
                row.innerHTML = `
                    <td>${sale.sale_date}</td>
                    <td>${sale.category}</td>
                    <td>$${sale.amount.toFixed(2)}</td>
                    <td>${sale.payment_method || '-'}</td>
                    <td>${sale.description || '-'}</td>
                `;
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 20px;">No sales recorded today</td></tr>';
        }
    } catch (error) {
        console.error('Error loading sales:', error);
    }
}

/**
 * Show sales form
 */
function showSalesForm() {
    const container = document.getElementById('salesFormContainer');
    if (container) {
        container.style.display = 'block';
        const form = document.getElementById('salesForm');
        if (form) form.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Hide sales form
 */
function hideSalesForm() {
    const container = document.getElementById('salesFormContainer');
    if (container) {
        container.style.display = 'none';
    }
}

/**
 * Setup sales form submission
 */
function setupSalesForm() {
    const salesForm = document.getElementById('salesForm');
    if (salesForm) {
        salesForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const saleDate = document.getElementById('saleDate')?.value;
            const category = document.getElementById('category')?.value;
            const amount = document.getElementById('amount')?.value;
            const description = document.getElementById('description')?.value;
            const paymentMethod = document.getElementById('paymentMethod')?.value;
            const transactionId = document.getElementById('transactionId')?.value;

            const saleData = {
                sale_date: saleDate,
                category: category,
                amount: parseFloat(amount),
                description: description,
                payment_method: paymentMethod,
                transaction_id: transactionId
            };

            try {
                await APIService.recordSale(saleData);
                alert('Sale recorded successfully!');
                hideSalesForm();
                salesForm.reset();
                initializeSalesPage();
            } catch (error) {
                alert('Error recording sale: ' + error.message);
            }
        });
    }
}

/**
 * Initialize rooms page
 */
async function initializeRoomsPage() {
    try {
        console.log('Initializing rooms page');
        const response = await APIService.getRooms();
        const grid = document.getElementById('roomsGrid');
        
        if (grid) {
            grid.innerHTML = '';

            if (response && response.rooms) {
                response.rooms.forEach(room => {
                    const card = document.createElement('div');
                    card.className = `room-card ${room.status.toLowerCase()}`;
                    card.innerHTML = `
                        <div class="room-number">${room.room_number}</div>
                        <div class="room-type">${room.room_type}</div>
                        <div class="room-price">$${room.price_per_night.toFixed(2)}/night</div>
                        <div class="room-status">${room.status}</div>
                    `;
                    card.style.cursor = 'pointer';
                    grid.appendChild(card);
                });
            }
        }

        // Load active check-ins
        const checkIns = await APIService.getActiveCheckIns();
        const tbody = document.getElementById('checkInsTable');
        
        if (tbody) {
            tbody.innerHTML = '';

            if (checkIns && checkIns.check_ins && checkIns.check_ins.length > 0) {
                checkIns.check_ins.forEach(checkIn => {
                    const row = tbody.insertRow();
                    row.innerHTML = `
                        <td>${checkIn.room_number}</td>
                        <td>${checkIn.guest_name}</td>
                        <td>${checkIn.check_in_date}</td>
                        <td>${checkIn.check_out_date}</td>
                        <td>${checkIn.number_of_guests}</td>
                        <td><button class="btn btn-sm btn-danger" onclick="checkoutGuest(${checkIn.room_id}, ${checkIn.check_in_id})">Check Out</button></td>
                    `;
                });
            } else {
                tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">No active check-ins</td></tr>';
            }
        }

        // Load available rooms for check-in form
        const available = await APIService.getAvailableRooms();
        const roomSelect = document.getElementById('roomSelect');
        
        if (roomSelect) {
            roomSelect.innerHTML = '<option value="">Select Room</option>';

            if (available && available.rooms) {
                available.rooms.forEach(room => {
                    const option = document.createElement('option');
                    option.value = room.room_id;
                    option.textContent = `${room.room_number} - ${room.room_type} ($${room.price_per_night.toFixed(2)})`;
                    roomSelect.appendChild(option);
                });
            }
        }
    } catch (error) {
        console.error('Error loading rooms:', error);
    }
}

/**
 * Show check-in form
 */
function showCheckInForm() {
    const container = document.getElementById('checkInFormContainer');
    if (container) {
        container.style.display = 'block';
        const form = document.getElementById('checkInForm');
        if (form) form.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Hide check-in form
 */
function hideCheckInForm() {
    const container = document.getElementById('checkInFormContainer');
    if (container) {
        container.style.display = 'none';
    }
}

/**
 * Checkout guest
 */
async function checkoutGuest(roomId, checkInId) {
    if (confirm('Are you sure you want to check out this guest?')) {
        try {
            await APIService.checkOutGuest(roomId, checkInId);
            alert('Guest checked out successfully!');
            initializeRoomsPage();
        } catch (error) {
            alert('Error checking out guest: ' + error.message);
        }
    }
}

/**
 * Setup check-in form
 */
function setupCheckInForm() {
    const checkInForm = document.getElementById('checkInForm');
    if (checkInForm) {
        checkInForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const roomId = document.getElementById('roomSelect')?.value;
            const checkInData = {
                guest_name: document.getElementById('guestName')?.value,
                check_in_date: document.getElementById('checkInDate')?.value,
                check_out_date: document.getElementById('checkOutDate')?.value,
                guest_email: document.getElementById('guestEmail')?.value,
                guest_phone: document.getElementById('guestPhone')?.value,
                number_of_guests: parseInt(document.getElementById('numberGuests')?.value || 1)
            };

            try {
                await APIService.checkInGuest(roomId, checkInData);
                alert('Guest checked in successfully!');
                hideCheckInForm();
                checkInForm.reset();
                initializeRoomsPage();
            } catch (error) {
                alert('Error checking in guest: ' + error.message);
            }
        });
    }
}

/**
 * Initialize employees page
 */
async function initializeEmployeesPage() {
    if (currentUser.role !== 'Admin' && currentUser.role !== 'Manager') {
        const container = document.getElementById('addEmployeeFormContainer');
        if (container) container.style.display = 'none';
        return;
    }

    try {
        console.log('Initializing employees page');
        const response = await APIService.getEmployees();
        const tbody = document.getElementById('employeesTable');
        
        if (tbody) {
            tbody.innerHTML = '';

            if (response && response.employees && response.employees.length > 0) {
                response.employees.forEach(employee => {
                    const row = tbody.insertRow();
                    row.innerHTML = `
                        <td>${employee.full_name}</td>
                        <td>${employee.username}</td>
                        <td>${employee.email}</td>
                        <td>${employee.role}</td>
                        <td>${employee.department || '-'}</td>
                        <td>${employee.is_active ? 'Active' : 'Inactive'}</td>
                    `;
                });
            }
        }
    } catch (error) {
        console.error('Error loading employees:', error);
    }
}

/**
 * Show add employee form
 */
function showAddEmployeeForm() {
    const container = document.getElementById('addEmployeeFormContainer');
    if (container) {
        container.style.display = 'block';
        const form = document.getElementById('addEmployeeForm');
        if (form) form.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Hide add employee form
 */
function hideAddEmployeeForm() {
    const container = document.getElementById('addEmployeeFormContainer');
    if (container) {
        container.style.display = 'none';
    }
}

/**
 * Setup add employee form
 */
function setupAddEmployeeForm() {
    const addEmpForm = document.getElementById('addEmployeeForm');
    if (addEmpForm) {
        addEmpForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const employeeData = {
                username: document.getElementById('empUsername')?.value,
                password: document.getElementById('empPassword')?.value,
                email: document.getElementById('empEmail')?.value,
                full_name: document.getElementById('empFullName')?.value,
                role: document.getElementById('empRole')?.value,
                department: document.getElementById('empDepartment')?.value
            };

            try {
                await APIService.createEmployee(employeeData);
                alert('Employee created successfully!');
                hideAddEmployeeForm();
                addEmpForm.reset();
                initializeEmployeesPage();
            } catch (error) {
                alert('Error creating employee: ' + error.message);
            }
        });
    }
}

/**
 * Initialize reports page
 */
function initializeReportsPage() {
    const today = new Date();
    const reportDateEl = document.getElementById('reportDate');
    if (reportDateEl) {
        reportDateEl.valueAsDate = today;
    }
}

/**
 * Handle report type change
 */
function handleReportChange() {
    const reportType = document.getElementById('reportType')?.value;
    const reportDate = document.getElementById('reportDate');
    
    if (reportType === 'yearly') {
        reportDate.type = 'number';
        reportDate.placeholder = 'Enter year';
        reportDate.value = new Date().getFullYear();
    } else {
        reportDate.type = 'date';
        reportDate.valueAsDate = new Date();
    }
}

/**
 * Generate report
 */
async function generateReport() {
    try {
        const reportType = document.getElementById('reportType')?.value;
        const reportDate = document.getElementById('reportDate')?.value;
        let reportContent = '';

        if (reportType === 'daily') {
            const response = await APIService.getDailyReport(reportDate);
            reportContent = generateDailyReportHTML(response.report);
        } else if (reportType === 'monthly') {
            const date = new Date(reportDate);
            const response = await APIService.getMonthlyReport(date.getFullYear(), date.getMonth() + 1);
            reportContent = generateMonthlyReportHTML(response.report);
        } else if (reportType === 'yearly') {
            const response = await APIService.getYearlyReport(reportDate);
            reportContent = generateYearlyReportHTML(response.report);
        }

        const contentEl = document.getElementById('reportContent');
        if (contentEl) {
            contentEl.innerHTML = reportContent;
        }
        
        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) {
            exportBtn.style.display = 'inline-block';
        }
    } catch (error) {
        console.error('Error generating report:', error);
        alert('Error generating report: ' + error.message);
    }
}

/**
 * Generate daily report HTML
 */
function generateDailyReportHTML(report) {
    if (!report) return '<p>No report data available</p>';
    
    let html = `
        <h3>Daily Sales Report - ${report.date}</h3>
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Sales</h3>
                <p class="stat-value">$${report.total_sales.toFixed(2)}</p>
            </div>
            <div class="stat-card">
                <h3>Transactions</h3>
                <p class="stat-value">${report.total_transactions}</p>
            </div>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Employee</th>
                    <th>Total Sales</th>
                    <th>Transactions</th>
                    <th>Avg. per Transaction</th>
                </tr>
            </thead>
            <tbody>
    `;

    if (report.employees && report.employees.length > 0) {
        report.employees.forEach(emp => {
            const avg = emp.transactions > 0 ? emp.total_sales / emp.transactions : 0;
            html += `
                <tr>
                    <td>${emp.employee_name}</td>
                    <td>$${emp.total_sales.toFixed(2)}</td>
                    <td>${emp.transactions}</td>
                    <td>$${avg.toFixed(2)}</td>
                </tr>
            `;
        });
    }

    html += `
            </tbody>
        </table>
    `;

    return html;
}

/**
 * Generate monthly report HTML
 */
function generateMonthlyReportHTML(report) {
    if (!report) return '<p>No report data available</p>';
    
    return `
        <h3>Monthly Sales Report - ${report.year}-${String(report.month).padStart(2, '0')}</h3>
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Sales</h3>
                <p class="stat-value">$${report.total_sales.toFixed(2)}</p>
            </div>
            <div class="stat-card">
                <h3>Total Transactions</h3>
                <p class="stat-value">${report.total_transactions}</p>
            </div>
        </div>
    `;
}

/**
 * Generate yearly report HTML
 */
function generateYearlyReportHTML(report) {
    if (!report) return '<p>No report data available</p>';
    
    let html = `
        <h3>Yearly Sales Report - ${report.year}</h3>
        <div class="stat-card">
            <h3>Total Annual Sales</h3>
            <p class="stat-value">$${report.total_sales.toFixed(2)}</p>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Month</th>
                    <th>Sales</th>
                </tr>
            </thead>
            <tbody>
    `;

    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    
    if (report.monthly_breakdown && report.monthly_breakdown.length > 0) {
        report.monthly_breakdown.forEach(month => {
            html += `
                <tr>
                    <td>${months[month.month - 1]}</td>
                    <td>$${month.total.toFixed(2)}</td>
                </tr>
            `;
        });
    }

    html += `
            </tbody>
        </table>
    `;

    return html;
}

/**
 * Export report
 */
function exportReport() {
    const reportType = document.getElementById('reportType')?.value;
    const reportDate = document.getElementById('reportDate')?.value;
    const format = document.getElementById('exportFormat')?.value;

    if (reportType === 'daily') {
        APIService.exportDailyReport(reportDate, format);
    } else if (reportType === 'monthly') {
        const date = new Date(reportDate);
        APIService.exportMonthlyReport(date.getFullYear(), date.getMonth() + 1, format);
    }
}

/**
 * Logout user
 */
async function logout() {
    console.log('Logging out');
    try {
        await APIService.logout();
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    APIService.clearToken();
    currentUser = null;
    showLoginPage();
}

/**
 * Initialize application on page load
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Initializing app');
    
    // Setup all forms
    setupSalesForm();
    setupCheckInForm();
    setupAddEmployeeForm();
    
    // Initialize app
    initApp();
});
