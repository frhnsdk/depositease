// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000';

// ==================== UTILITY FUNCTIONS ====================

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'API request failed');
        }
        
        // Handle 204 No Content
        if (response.status === 204) {
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        alert('Error: ' + error.message);
        throw error;
    }
}

// ==================== TAB FUNCTIONALITY ====================

document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            document.getElementById(tabName).classList.add('active');
            
            // Load data based on tab
            if (tabName === 'applications') {
                loadApplications();
            } else if (tabName === 'products') {
                loadProducts();
            } else if (tabName === 'banks') {
                loadBanks();
            }
        });
    });
    
    // Load initial data if on admin page
    if (window.location.pathname.includes('admin')) {
        loadDashboardStats();
        loadApplications();
    }
    
    // Search functionality (placeholder)
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            console.log('Searching for:', e.target.value);
            // Add search logic here
        });
    }
    
    // Filter functionality (placeholder)
    const typeFilter = document.getElementById('typeFilter');
    const tenureFilter = document.getElementById('tenureFilter');
    
    if (typeFilter) {
        typeFilter.addEventListener('change', function(e) {
            console.log('Filter by type:', e.target.value);
            // Add filter logic here
        });
    }
    
    if (tenureFilter) {
        tenureFilter.addEventListener('change', function(e) {
            console.log('Filter by tenure:', e.target.value);
            // Add filter logic here
        });
    }
});

// ==================== DASHBOARD STATS ====================

async function loadDashboardStats() {
    try {
        const stats = await apiRequest('/stats/dashboard');
        
        document.querySelector('.stat-card:nth-child(1) .stat-value').textContent = stats.total_banks;
        document.querySelector('.stat-card:nth-child(2) .stat-value').textContent = stats.total_products;
        document.querySelector('.stat-card:nth-child(3) .stat-value').textContent = stats.pending_applications;
        document.querySelector('.stat-card:nth-child(4) .stat-value').textContent = stats.approved_today;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// ==================== BANK FUNCTIONS ====================

async function loadBanks() {
    try {
        const banks = await apiRequest('/banks');
        displayBanks(banks);
    } catch (error) {
        console.error('Failed to load banks:', error);
    }
}

function displayBanks(banks) {
    const tbody = document.querySelector('#banks tbody');
    if (!tbody) return;
    
    tbody.innerHTML = banks.map(bank => `
        <tr>
            <td>${bank.name}</td>
            <td>${bank.products ? bank.products.length : 0} products</td>
            <td class="action-btns">
                <button class="action-btn" onclick="editBank(${bank.id})" title="Edit">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                        <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13" stroke="#6B7280" stroke-width="2" stroke-linecap="round"/>
                        <path d="M18.5 2.50001C18.8978 2.10219 19.4374 1.87869 20 1.87869C20.5626 1.87869 21.1022 2.10219 21.5 2.50001C21.8978 2.89784 22.1213 3.4374 22.1213 4.00001C22.1213 4.56262 21.8978 5.10219 21.5 5.50001L12 15L8 16L9 12L18.5 2.50001Z" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
                <button class="action-btn delete-btn" onclick="deleteBank(${bank.id})" title="Delete">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                        <path d="M3 6H5H21" stroke="#EF4444" stroke-width="2" stroke-linecap="round"/>
                        <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="#EF4444" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>
            </td>
        </tr>
    `).join('');
}

// ==================== MODAL FUNCTIONS ====================

let currentBankId = null;
let currentProductId = null;

function openBankModal(bankId = null) {
    currentBankId = bankId;
    const modal = document.getElementById('bankModal');
    const title = document.getElementById('bankModalTitle');
    const btnText = document.getElementById('bankBtnText');
    
    if (bankId) {
        title.textContent = 'Edit Bank';
        btnText.textContent = 'Update Bank';
        loadBankData(bankId);
    } else {
        title.textContent = 'Add Bank';
        btnText.textContent = 'Save Bank';
        document.getElementById('bankForm').reset();
    }
    
    modal.classList.add('active');
}

function closeBankModal() {
    document.getElementById('bankModal').classList.remove('active');
    document.getElementById('bankForm').reset();
    currentBankId = null;
}

async function loadBankData(bankId) {
    try {
        const bank = await apiRequest(`/banks/${bankId}`);
        document.getElementById('bankName').value = bank.name;
        document.getElementById('bankDescription').value = bank.description || '';
        document.getElementById('bankWebsite').value = bank.website || '';
        document.getElementById('bankContact').value = bank.contact_number || '';
        document.getElementById('bankEmail').value = bank.email || '';
    } catch (error) {
        console.error('Failed to load bank data:', error);
    }
}

async function saveBankForm() {
    const form = document.getElementById('bankForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const btn = document.getElementById('saveBankBtn');
    const btnText = document.getElementById('bankBtnText');
    btn.disabled = true;
    btnText.innerHTML = '<span class="loading"></span>Saving...';
    
    const data = {
        name: document.getElementById('bankName').value,
        description: document.getElementById('bankDescription').value || null,
        website: document.getElementById('bankWebsite').value || null,
        contact_number: document.getElementById('bankContact').value || null,
        email: document.getElementById('bankEmail').value || null,
        is_active: true
    };
    
    try {
        if (currentBankId) {
            await apiRequest(`/banks/${currentBankId}`, 'PUT', data);
            alert('Bank updated successfully!');
        } else {
            await apiRequest('/banks', 'POST', data);
            alert('Bank added successfully!');
        }
        
        closeBankModal();
        loadBanks();
        loadDashboardStats();
    } catch (error) {
        console.error('Failed to save bank:', error);
    } finally {
        btn.disabled = false;
        btnText.textContent = currentBankId ? 'Update Bank' : 'Save Bank';
    }
}

function openProductModal(productId = null) {
    currentProductId = productId;
    const modal = document.getElementById('productModal');
    const title = document.getElementById('productModalTitle');
    const btnText = document.getElementById('productBtnText');
    
    loadBanksForSelect();
    
    if (productId) {
        title.textContent = 'Edit Product';
        btnText.textContent = 'Update Product';
        loadProductData(productId);
    } else {
        title.textContent = 'Add Product';
        btnText.textContent = 'Save Product';
        document.getElementById('productForm').reset();
    }
    
    modal.classList.add('active');
}

function closeProductModal() {
    document.getElementById('productModal').classList.remove('active');
    document.getElementById('productForm').reset();
    currentProductId = null;
}

async function loadBanksForSelect() {
    try {
        const banks = await apiRequest('/banks');
        const select = document.getElementById('productBank');
        select.innerHTML = '<option value="">Choose a bank...</option>';
        banks.forEach(bank => {
            const option = document.createElement('option');
            option.value = bank.id;
            option.textContent = bank.name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Failed to load banks:', error);
    }
}

async function loadProductData(productId) {
    try {
        const product = await apiRequest(`/products/${productId}`);
        document.getElementById('productBank').value = product.bank_id;
        document.getElementById('productName').value = product.name;
        document.getElementById('productType').value = product.type;
        document.getElementById('productRate').value = product.interest_rate;
        document.getElementById('productMinDeposit').value = product.min_deposit;
        document.getElementById('productMaxDeposit').value = product.max_deposit || '';
        document.getElementById('productTenure').value = product.tenure;
        document.getElementById('productOverview').value = product.product_overview || '';
        document.getElementById('productFeatures').value = product.key_features || '';
        document.getElementById('productWithdrawal').value = product.withdrawal_rules || '';
        document.getElementById('productEligibility').value = product.eligibility_criteria || '';
        document.getElementById('productDocuments').value = product.required_documents || '';
        document.getElementById('productCompounding').value = product.compounding_frequency || '';
        document.getElementById('productPenalty').value = product.premature_withdrawal_penalty || '';
    } catch (error) {
        console.error('Failed to load product data:', error);
    }
}

async function saveProductForm() {
    const form = document.getElementById('productForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    const btn = document.getElementById('saveProductBtn');
    const btnText = document.getElementById('productBtnText');
    btn.disabled = true;
    btnText.innerHTML = '<span class="loading"></span>Saving...';
    
    const data = {
        bank_id: parseInt(document.getElementById('productBank').value),
        name: document.getElementById('productName').value,
        type: document.getElementById('productType').value,
        interest_rate: parseFloat(document.getElementById('productRate').value),
        min_deposit: parseFloat(document.getElementById('productMinDeposit').value),
        max_deposit: parseFloat(document.getElementById('productMaxDeposit').value) || null,
        tenure: document.getElementById('productTenure').value,
        product_overview: document.getElementById('productOverview').value || null,
        key_features: document.getElementById('productFeatures').value || null,
        withdrawal_rules: document.getElementById('productWithdrawal').value || null,
        eligibility_criteria: document.getElementById('productEligibility').value || null,
        required_documents: document.getElementById('productDocuments').value || null,
        compounding_frequency: document.getElementById('productCompounding').value || null,
        premature_withdrawal_penalty: document.getElementById('productPenalty').value || null,
        is_active: true
    };
    
    try {
        if (currentProductId) {
            await apiRequest(`/products/${currentProductId}`, 'PUT', data);
            alert('Product updated successfully!');
        } else {
            await apiRequest('/products', 'POST', data);
            alert('Product added successfully!');
        }
        
        closeProductModal();
        loadProducts();
        loadDashboardStats();
    } catch (error) {
        console.error('Failed to save product:', error);
    } finally {
        btn.disabled = false;
        btnText.textContent = currentProductId ? 'Update Product' : 'Save Product';
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const bankModal = document.getElementById('bankModal');
    const productModal = document.getElementById('productModal');
    
    if (event.target === bankModal) {
        closeBankModal();
    }
    if (event.target === productModal) {
        closeProductModal();
    }
}

function addBank() {
    openBankModal();
}

function editBank(bankId) {
    openBankModal(bankId);
}

async function deleteBank(bankId) {
    if (!confirm('Are you sure you want to delete this bank? All associated products will be deleted.')) {
        return;
    }
    
    try {
        await apiRequest(`/banks/${bankId}`, 'DELETE');
        alert('Bank deleted successfully!');
        loadBanks();
        loadDashboardStats();
    } catch (error) {
        console.error('Failed to delete bank:', error);
    }
}

// ==================== PRODUCT FUNCTIONS ====================

async function loadProducts() {
    try {
        const products = await apiRequest('/products');
        displayProducts(products);
    } catch (error) {
        console.error('Failed to load products:', error);
    }
}

function displayProducts(products) {
    const tbody = document.querySelector('#products tbody');
    if (!tbody) return;
    
    tbody.innerHTML = products.map(product => `
        <tr>
            <td>${product.bank.name}</td>
            <td>${product.type}</td>
            <td>${product.interest_rate}%</td>
            <td>৳${product.min_deposit.toLocaleString()}</td>
            <td>${product.tenure}</td>
            <td class="action-btns">
                <button class="action-btn" onclick="editProduct(${product.id})" title="Edit">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                        <path d="M11 4H4C3.46957 4 2.96086 4.21071 2.58579 4.58579C2.21071 4.96086 2 5.46957 2 6V20C2 20.5304 2.21071 21.0391 2.58579 21.4142C2.96086 21.7893 3.46957 22 4 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V13" stroke="#6B7280" stroke-width="2" stroke-linecap="round"/>
                        <path d="M18.5 2.50001C18.8978 2.10219 19.4374 1.87869 20 1.87869C20.5626 1.87869 21.1022 2.10219 21.5 2.50001C21.8978 2.89784 22.1213 3.4374 22.1213 4.00001C22.1213 4.56262 21.8978 5.10219 21.5 5.50001L12 15L8 16L9 12L18.5 2.50001Z" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
                <button class="action-btn delete-btn" onclick="deleteProduct(${product.id})" title="Delete">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                        <path d="M3 6H5H21" stroke="#EF4444" stroke-width="2" stroke-linecap="round"/>
                        <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="#EF4444" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>
            </td>
        </tr>
    `).join('');
}

async function addProduct() {
    try {
        const banks = await apiRequest('/banks');
        
        if (banks.length === 0) {
            alert('Please add a bank first!');
            return;
        }
        
        openProductModal();
    } catch (error) {
        console.error('Failed to add product:', error);
    }
}

function editProduct(productId) {
    openProductModal(productId);
}

async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }
    
    try {
        await apiRequest(`/products/${productId}`, 'DELETE');
        alert('Product deleted successfully!');
        loadProducts();
        loadDashboardStats();
    } catch (error) {
        console.error('Failed to delete product:', error);
    }
}

// ==================== APPLICATION FUNCTIONS ====================

async function loadApplications() {
    try {
        const applications = await apiRequest('/applications');
        displayApplications(applications);
    } catch (error) {
        console.error('Failed to load applications:', error);
    }
}

function displayApplications(applications) {
    const tbody = document.querySelector('#applications tbody');
    if (!tbody) return;
    
    tbody.innerHTML = applications.map(app => {
        const date = new Date(app.created_at).toLocaleDateString();
        return `
        <tr>
            <td>${app.applicant_name}</td>
            <td>Product ID: ${app.product_id}</td>
            <td>${app.phone}</td>
            <td>${date}</td>
            <td><span class="status-badge ${app.status}">${app.status}</span></td>
            <td class="action-btns">
                <button class="action-btn" onclick="viewApplication(${app.id})" title="View">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                        <path d="M15 12C15 13.6569 13.6569 15 12 15C10.3431 15 9 13.6569 9 12C9 10.3431 10.3431 9 12 9C13.6569 9 15 10.3431 15 12Z" stroke="#6B7280" stroke-width="2"/>
                        <path d="M2 12C2 12 5 5 12 5C19 5 22 12 22 12C22 12 19 19 12 19C5 19 2 12 2 12Z" stroke="#6B7280" stroke-width="2"/>
                    </svg>
                </button>
                ${app.status === 'pending' ? `
                <button class="action-btn" onclick="updateApplicationStatus(${app.id}, 'approved')" title="Approve" style="color: green;">
                    ✓
                </button>
                <button class="action-btn delete-btn" onclick="updateApplicationStatus(${app.id}, 'rejected')" title="Reject">
                    ✗
                </button>
                ` : ''}
            </td>
        </tr>
    `}).join('');
}

async function viewApplication(appId) {
    try {
        const application = await apiRequest(`/applications/${appId}`);
        
        // Populate modal with application details
        document.getElementById('appName').textContent = application.applicant_name;
        document.getElementById('appPhone').textContent = application.phone;
        document.getElementById('appEmail').textContent = application.email || 'N/A';
        document.getElementById('appNID').textContent = application.nid_number || 'N/A';
        document.getElementById('appAddress').textContent = application.address || 'N/A';
        
        // Product info
        const productName = application.product ? 
            `${application.product.name} (${application.product.type})` : 
            `Product ID: ${application.product_id}`;
        document.getElementById('appProduct').textContent = productName;
        document.getElementById('appDeposit').textContent = application.deposit_amount ? 
            `৳${formatNumber(application.deposit_amount)}` : 'N/A';
        document.getElementById('appTenure').textContent = application.tenure_selected;
        
        // Status badge
        const statusEl = document.getElementById('appStatus');
        statusEl.textContent = application.status.toUpperCase();
        statusEl.style.color = application.status === 'approved' ? '#10b981' : 
                              application.status === 'rejected' ? '#ef4444' : '#f59e0b';
        statusEl.style.fontWeight = '700';
        
        // Date
        document.getElementById('appDate').textContent = 
            new Date(application.created_at).toLocaleString();
        
        // Notes
        const notesSection = document.getElementById('appNotesSection');
        if (application.notes) {
            document.getElementById('appNotes').textContent = application.notes;
            notesSection.style.display = 'block';
        } else {
            notesSection.style.display = 'none';
        }
        
        // Review info
        const reviewSection = document.getElementById('appReviewSection');
        if (application.reviewed_by) {
            document.getElementById('appReviewedBy').textContent = application.reviewed_by;
            document.getElementById('appReviewedAt').textContent = 
                new Date(application.reviewed_at).toLocaleString();
            reviewSection.style.display = 'block';
        } else {
            reviewSection.style.display = 'none';
        }
        
        // Show modal
        document.getElementById('applicationModal').classList.add('active');
    } catch (error) {
        console.error('Failed to load application:', error);
        alert('Failed to load application details');
    }
}

function closeApplicationModal() {
    document.getElementById('applicationModal').classList.remove('active');
}

async function updateApplicationStatus(appId, status) {
    try {
        await apiRequest(`/applications/${appId}`, 'PUT', {
            status: status,
            reviewed_by: 'Admin'
        });
        
        alert(`Application ${status} successfully!`);
        loadApplications();
        loadDashboardStats();
    } catch (error) {
        console.error('Failed to update application:', error);
    }
}

// ==================== HOME PAGE FUNCTIONS ====================

// Load and display products on home page
async function loadHomeProducts() {
    try {
        const searchInput = document.getElementById('searchInput');
        const typeFilter = document.getElementById('typeFilter');
        const tenureFilter = document.getElementById('tenureFilter');
        
        if (!searchInput || !typeFilter || !tenureFilter) return;
        
        // Add event listeners for filters
        searchInput.addEventListener('input', filterProducts);
        typeFilter.addEventListener('change', filterProducts);
        tenureFilter.addEventListener('change', filterProducts);
        
        // Initial load
        await filterProducts();
    } catch (error) {
        console.error('Failed to load home products:', error);
    }
}

async function filterProducts() {
    try {
        const searchInput = document.getElementById('searchInput').value.toLowerCase();
        const typeFilter = document.getElementById('typeFilter').value;
        const tenureFilter = document.getElementById('tenureFilter').value;
        
        // Build query params - only use type filter for backend
        let endpoint = '/products?';
        if (typeFilter) endpoint += `type=${encodeURIComponent(typeFilter)}&`;
        
        const products = await apiRequest(endpoint);
        
        // Filter on frontend
        let filteredProducts = products;
        
        // Filter by search term (bank name)
        if (searchInput) {
            filteredProducts = filteredProducts.filter(p => 
                p.bank.name.toLowerCase().includes(searchInput)
            );
        }
        
        // Filter by tenure (flexible matching)
        if (tenureFilter) {
            filteredProducts = filteredProducts.filter(p => {
                const productTenure = p.tenure.toLowerCase();
                const selectedTenure = tenureFilter.toLowerCase();
                
                // Extract numbers from both
                const productMonths = parseInt(productTenure);
                const selectedMonths = parseInt(selectedTenure);
                
                // Match if the months are equal
                return productMonths === selectedMonths;
            });
        }
        
        displayHomeProducts(filteredProducts);
    } catch (error) {
        console.error('Failed to filter products:', error);
        document.getElementById('productsGrid').innerHTML = 
            '<p style="text-align: center; grid-column: 1/-1;">Failed to load products</p>';
    }
}

function displayHomeProducts(products) {
    const grid = document.getElementById('productsGrid');
    const countEl = document.getElementById('productCount');
    
    if (!grid) return;
    
    if (countEl) {
        countEl.textContent = `${products.length} product${products.length !== 1 ? 's' : ''} found`;
    }
    
    if (products.length === 0) {
        grid.innerHTML = '<p style="text-align: center; grid-column: 1/-1; color: #6b7280;">No products found</p>';
        return;
    }
    
    grid.innerHTML = products.map(product => {
        const keyFeatures = product.key_features ? 
            product.key_features.split('|').slice(0, 3) : [];
        
        return `
            <div class="product-card" onclick="viewProductDetails(${product.id})">
                <div class="product-card-header">
                    <div class="product-card-icon">🏦</div>
                    <div class="product-card-title">
                        <div class="product-bank-name">${escapeHtml(product.bank.name)}</div>
                        <span class="product-type-badge">${escapeHtml(product.type)}</span>
                    </div>
                </div>
                
                <div class="product-rate">${product.interest_rate}%</div>
                <span class="product-rate-label">per annum</span>
                
                <div class="product-details">
                    <div class="product-detail-item">
                        <div class="product-detail-label">Min. Deposit</div>
                        <div class="product-detail-value">৳${formatNumber(product.min_deposit)}</div>
                    </div>
                    <div class="product-detail-item">
                        <div class="product-detail-label">Tenure</div>
                        <div class="product-detail-value">${product.tenure}</div>
                    </div>
                </div>
                
                ${keyFeatures.length > 0 ? `
                    <div class="product-features">
                        <ul>
                            ${keyFeatures.map(f => `<li>${escapeHtml(f.trim())}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                <div class="product-card-actions">
                    <button class="btn btn-outline" onclick="event.stopPropagation(); viewProductDetails(${product.id})">View Details</button>
                    <button class="btn btn-primary" onclick="event.stopPropagation(); applyForProduct(${product.id})">Apply Now</button>
                </div>
            </div>
        `;
    }).join('');
}

function viewProductDetails(productId) {
    window.location.href = `/product-details.html?id=${productId}`;
}

function applyForProduct(productId) {
    window.location.href = `/application.html?id=${productId}`;
}

// ==================== PRODUCT DETAILS PAGE FUNCTIONS ====================

async function loadProductDetails(productId) {
    try {
        const product = await apiRequest(`/products/${productId}`);
        
        // Header
        document.getElementById('bankName').textContent = product.bank.name;
        document.getElementById('productType').textContent = product.type;
        document.getElementById('interestRate').textContent = `${product.interest_rate}%`;
        document.getElementById('interestRateSidebar').textContent = `${product.interest_rate}% p.a.`;
        
        // Overview
        document.getElementById('productOverview').textContent = 
            product.product_overview || 'No overview available';
        
        // Key Features
        const features = product.key_features ? product.key_features.split('|') : [];
        const featuresList = document.getElementById('keyFeaturesList');
        featuresList.innerHTML = features.length > 0 ?
            features.map(f => `<li>${escapeHtml(f.trim())}</li>`).join('') :
            '<li>No features listed</li>';
        
        // Withdrawal Rules
        document.getElementById('withdrawalRules').textContent = 
            product.withdrawal_rules || 'Standard withdrawal rules apply';
        
        // Eligibility
        document.getElementById('eligibilityCriteria').textContent = 
            product.eligibility_criteria || 'Contact bank for eligibility details';
        
        // Required Documents
        const docs = product.required_documents ? product.required_documents.split('|') : [];
        const docsList = document.getElementById('requiredDocsList');
        docsList.innerHTML = docs.length > 0 ?
            docs.map(d => `<li>${escapeHtml(d.trim())}</li>`).join('') :
            '<li>Contact bank for document requirements</li>';
        
        // Quick Facts
        document.getElementById('minDeposit').textContent = `৳${formatNumber(product.min_deposit)}`;
        document.getElementById('tenure').textContent = product.tenure;
        
        // Compounding frequency (optional field)
        if (product.compounding_frequency) {
            document.getElementById('compounding').textContent = product.compounding_frequency;
            document.getElementById('compoundingItem').style.display = 'flex';
        }
        
        // Calculate estimated returns
        const rate = parseFloat(product.interest_rate) / 100;
        const tenureInYears = parseTenureToYears(product.tenure);
        
        document.getElementById('return10k').textContent = 
            `৳${formatNumber(calculateMaturityAmount(10000, rate, tenureInYears))}`;
        document.getElementById('return50k').textContent = 
            `৳${formatNumber(calculateMaturityAmount(50000, rate, tenureInYears))}`;
        document.getElementById('return100k').textContent = 
            `৳${formatNumber(calculateMaturityAmount(100000, rate, tenureInYears))}`;
        
    } catch (error) {
        console.error('Failed to load product details:', error);
        alert('Failed to load product details');
        window.location.href = '/';
    }
}

function goToApplication() {
    const urlParams = new URLSearchParams(window.location.search);
    const productId = urlParams.get('id');
    if (productId) {
        window.location.href = `/application.html?id=${productId}`;
    }
}

// ==================== APPLICATION PAGE FUNCTIONS ====================

async function loadProductForApplication(productId) {
    try {
        const product = await apiRequest(`/products/${productId}`);
        
        // Update page title
        document.getElementById('productName').textContent = 
            `${product.bank.name}'s ${product.type}`;
        
        // Fill selected product sidebar
        document.getElementById('selectedBank').textContent = product.bank.name;
        document.getElementById('selectedType').textContent = product.type;
        document.getElementById('selectedRate').textContent = `${product.interest_rate}%`;
        document.getElementById('selectedMinDeposit').textContent = 
            `৳${formatNumber(product.min_deposit)}`;
        document.getElementById('selectedTenure').textContent = product.tenure;
        
        // Set tenure in form (readonly)
        document.getElementById('tenureSelected').value = product.tenure;
        
        // Set up form submission
        const form = document.getElementById('applicationForm');
        form.onsubmit = async (e) => {
            e.preventDefault();
            await submitApplication(productId);
        };
        
    } catch (error) {
        console.error('Failed to load product:', error);
        alert('Failed to load product details');
        window.location.href = '/';
    }
}

async function submitApplication(productId) {
    const submitBtn = document.getElementById('submitBtn');
    const submitBtnText = document.getElementById('submitBtnText');
    
    try {
        // Disable button
        submitBtn.disabled = true;
        submitBtnText.textContent = 'Submitting...';
        
        const applicationData = {
            product_id: parseInt(productId),
            applicant_name: document.getElementById('applicantName').value,
            phone: document.getElementById('applicantPhone').value,
            email: document.getElementById('applicantEmail').value,
            nid_number: document.getElementById('applicantNID').value || null,
            address: document.getElementById('applicantAddress').value || null,
            deposit_amount: parseFloat(document.getElementById('depositAmount').value) || null,
            tenure_selected: document.getElementById('tenureSelected').value,
            notes: document.getElementById('applicationNotes').value || null,
            status: 'pending'
        };
        
        await apiRequest('/applications', 'POST', applicationData);
        
        alert('Application submitted successfully! Our team will contact you within 24-48 hours.');
        window.location.href = '/';
        
    } catch (error) {
        console.error('Failed to submit application:', error);
        submitBtn.disabled = false;
        submitBtnText.textContent = 'Submit Application';
    }
}

// ==================== HELPER FUNCTIONS ====================

function formatNumber(num) {
    if (!num) return '0';
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function calculateMaturityAmount(principal, rate, years) {
    // Simple interest calculation
    return Math.round(principal + (principal * rate * years));
}

function parseTenureToYears(tenure) {
    if (!tenure) return 1;
    
    tenure = tenure.toLowerCase();
    
    if (tenure.includes('month')) {
        const months = parseInt(tenure);
        return months / 12;
    } else if (tenure.includes('year')) {
        return parseInt(tenure);
    }
    
    // Default to 1 year
    return 1;
}

// ==================== LOGOUT FUNCTION ====================

async function logout() {
    try {
        await fetch(`${API_BASE_URL}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        });
        window.location.href = '/login';
    } catch (error) {
        console.error('Logout error:', error);
        window.location.href = '/login';
    }
}

// ==================== INITIALIZE ====================

// Check which page we're on and initialize accordingly
if (document.getElementById('productsGrid')) {
    // Home page
    document.addEventListener('DOMContentLoaded', loadHomeProducts);
}
