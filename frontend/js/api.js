// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Get token from localStorage
const getToken = () => localStorage.getItem('auth_token');

// Set token to localStorage
const setToken = (token) => localStorage.setItem('auth_token', token);

// Remove token from localStorage
const removeToken = () => localStorage.removeItem('auth_token');

// Get user info from localStorage
const getUserInfo = () => {
    const userStr = localStorage.getItem('user_info');
    return userStr ? JSON.parse(userStr) : null;
};

// Set user info to localStorage
const setUserInfo = (user) => {
    localStorage.setItem('user_info', JSON.stringify(user));
};

// Remove user info from localStorage
const removeUserInfo = () => {
    localStorage.removeItem('user_info');
};

// Check if user is authenticated
const isAuthenticated = () => {
    return !!getToken();
};

// API Request Helper with Token
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }

    const config = {
        ...options,
        headers,
    };

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        
        if (response.status === 401) {
            // Token invalid atau expired
            removeToken();
            removeUserInfo();
            updateAuthUI();
            showAlert('Session expired. Please login again.', 'error');
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
            return null;
        }

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Login function
async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (!response.ok) {
            // Handle different error formats from DRF
            let errorMessage = 'Login failed';
            if (data.non_field_errors) {
                errorMessage = data.non_field_errors[0];
            } else if (data.detail) {
                errorMessage = data.detail;
            } else if (data.username) {
                errorMessage = `Username: ${data.username[0]}`;
            } else if (data.password) {
                errorMessage = `Password: ${data.password[0]}`;
            }
            throw new Error(errorMessage);
        }

        setToken(data.token);
        setUserInfo({
            user_id: data.user_id,
            username: data.username,
            email: data.email,
        });
        
        return data;
    } catch (error) {
        console.error('Login Error:', error);
        throw error;
    }
}

// Logout function
async function logout() {
    try {
        const token = getToken();
        if (token) {
            await fetch(`${API_BASE_URL}/auth/logout/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                },
            });
        }
    } catch (error) {
        console.error('Logout Error:', error);
    } finally {
        removeToken();
        removeUserInfo();
        updateAuthUI();
        window.location.href = 'login.html';
    }
}

// Update Auth UI (Navbar)
function updateAuthUI() {
    const authSection = document.getElementById('authSection');
    const userInfo = getUserInfo();

    if (authSection) {
        if (isAuthenticated() && userInfo) {
            authSection.innerHTML = `
                <span id="userInfo">Welcome, ${userInfo.username}</span>
                <button onclick="logout()" class="btn btn-secondary">Logout</button>
            `;
        } else {
            authSection.innerHTML = `
                <a href="login.html" class="btn btn-primary">Login</a>
            `;
        }
    }
}

// Show Alert Message
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    }
}

// Show Loading Spinner
function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Loading...</p>
            </div>
        `;
    }
}

// Format Date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('id-ID', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
}

// Format Time
function formatTime(timeString) {
    return timeString.substring(0, 5); // HH:MM
}

// Get Image URL
function getImageUrl(imagePath) {
    if (!imagePath) return null;
    if (imagePath.startsWith('http')) return imagePath;
    return `http://localhost:8000${imagePath}`;
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialize Auth on Page Load
document.addEventListener('DOMContentLoaded', () => {
    updateAuthUI();
    
    // Highlight active menu
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const menuLinks = document.querySelectorAll('.navbar-menu a');
    menuLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});
