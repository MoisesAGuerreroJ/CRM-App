async function fetchAppConfig() {
    try {
        const response = await fetch('/app-config');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error('Unable to load local application configuration:', error);
        return {};
    }
}

function applyAppConfig(config) {
    const appTitle = config.app_title || 'CRM Application';
    document.title = appTitle;
    document.querySelectorAll('header h1').forEach(element => {
        element.textContent = appTitle;
    });

    const formTitle = config.form_title || 'Customer Registration';
    const formTitleElement = document.getElementById('form-title');
    if (formTitleElement) formTitleElement.textContent = formTitle;

    populateConfiguredOptions('regalo-deseado', config.gift_options || []);
    populateConfiguredOptions('distribucion', config.distribution_options || []);
}

function populateConfiguredOptions(selectId, options) {
    const select = document.getElementById(selectId);
    if (!select) return;
    select.replaceChildren(new Option('Select an option', ''));
    options.forEach(option => {
        if (option && typeof option.value === 'string' && typeof option.label === 'string') {
            select.add(new Option(option.label, option.value));
        }
    });
}

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, character => ({
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    })[character]);
}
