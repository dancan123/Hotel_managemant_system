/**
 * API Service Module
 * Handles all backend API communication
 */

const API_BASE_URL = 'http://localhost:5000/api';
let authToken = null;

class APIService {
    /**
     * Set the authentication token
     */
    static setToken(token) {
        authToken = token;
        localStorage.setItem('authToken', token);
    }

    /**
     * Get the authentication token
     */
    static getToken() {
        if (!authToken) {
            authToken = localStorage.getItem('authToken');
        }
        return authToken;
    }

    /**
     * Clear the authentication token
     */
    static clearToken() {
        authToken = null;
        localStorage.removeItem('authToken');
    }

    /**
     * Make an API request
     */
    static async request(endpoint, method = 'GET', data = null) {
        const url = `${API_BASE_URL}${endpoint}`;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        const token = this.getToken();
        if (token) {
            options.headers['Authorization'] = `Bearer ${token}`;
        }

        if (data) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);
            const result = await response.json();

            if (!response.ok) {
                if (response.status === 401) {
                    this.clearToken();
                    window.location.href = '/';
                }
                throw new Error(result.error || 'API Error');
            }

            return result;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Authentication
    static login(username, password) {
        return this.request('/auth/login', 'POST', { username, password });
    }

    static logout() {
        return this.request('/auth/logout', 'POST');
    }

    static verifyToken() {
        return this.request('/auth/verify-token', 'POST');
    }

    static getProfile() {
        return this.request('/auth/profile', 'GET');
    }

    // Sales
    static recordSale(saleData) {
        return this.request('/sales/record', 'POST', saleData);
    }

    static getDailySales(employeeId, date) {
        return this.request(`/sales/daily/${employeeId}/${date}`, 'GET');
    }

    static getMonthlySales(year, month, employeeId = null) {
        let endpoint = `/sales/monthly/${year}/${month}`;
        if (employeeId) {
            endpoint += `?employee_id=${employeeId}`;
        }
        return this.request(endpoint, 'GET');
    }

    static getDailySummary(date) {
        return this.request(`/sales/daily-summary/${date}`, 'GET');
    }

    static getEmployeePerformance(employeeId) {
        return this.request(`/sales/employee-performance/${employeeId}`, 'GET');
    }

    static getSaleCategories() {
        return this.request('/sales/categories', 'GET');
    }

    static getPaymentMethods() {
        return this.request('/sales/payment-methods', 'GET');
    }

    // Employees
    static getEmployees(role = null) {
        let endpoint = '/employees/';
        if (role) {
            endpoint += `?role=${role}`;
        }
        return this.request(endpoint, 'GET');
    }

    static getEmployee(employeeId) {
        return this.request(`/employees/${employeeId}`, 'GET');
    }

    static createEmployee(employeeData) {
        return this.request('/employees/', 'POST', employeeData);
    }

    static updateEmployee(employeeId, employeeData) {
        return this.request(`/employees/${employeeId}`, 'PUT', employeeData);
    }

    static deactivateEmployee(employeeId) {
        return this.request(`/employees/${employeeId}/deactivate`, 'PUT');
    }

    // Rooms
    static getRooms() {
        return this.request('/rooms/', 'GET');
    }

    static getAvailableRooms() {
        return this.request('/rooms/available', 'GET');
    }

    static createRoom(roomData) {
        return this.request('/rooms/', 'POST', roomData);
    }

    static checkInGuest(roomId, checkInData) {
        return this.request(`/rooms/${roomId}/check-in`, 'POST', checkInData);
    }

    static checkOutGuest(roomId, checkInId) {
        return this.request(`/rooms/${roomId}/check-out`, 'POST', { check_in_id: checkInId });
    }

    static getActiveCheckIns() {
        return this.request('/rooms/active-check-ins', 'GET');
    }

    static getOccupancyReport() {
        return this.request('/rooms/occupancy-report', 'GET');
    }

    // Dashboard
    static getDashboardOverview() {
        return this.request('/dashboard/overview', 'GET');
    }

    static getSalesTrend(days) {
        return this.request(`/dashboard/sales-trend/${days}`, 'GET');
    }

    static getEmployeeLeaderboard(days = 30) {
        return this.request(`/dashboard/employee-leaderboard?days=${days}`, 'GET');
    }

    static getCategoryBreakdown(date) {
        return this.request(`/dashboard/category-breakdown/${date}`, 'GET');
    }

    static getPaymentBreakdown(date) {
        return this.request(`/dashboard/payment-method-breakdown/${date}`, 'GET');
    }

    // Reports
    static getDailyReport(date) {
        return this.request(`/reports/daily/${date}`, 'GET');
    }

    static getMonthlyReport(year, month) {
        return this.request(`/reports/monthly/${year}/${month}`, 'GET');
    }

    static getYearlyReport(year) {
        return this.request(`/reports/yearly/${year}`, 'GET');
    }

    static getEmployeeReport(employeeId, period) {
        return this.request(`/reports/employee-performance/${employeeId}/${period}`, 'GET');
    }

    static exportDailyReport(date, format) {
        window.location.href = `${API_BASE_URL}/reports/export/daily/${date}?format=${format}`;
    }

    static exportMonthlyReport(year, month, format) {
        window.location.href = `${API_BASE_URL}/reports/export/monthly/${year}/${month}?format=${format}`;
    }
}
