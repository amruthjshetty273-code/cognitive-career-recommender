// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    try {
        // Check for hash in URL and activate appropriate tab
        function handleInitialTab() {
            try {
                const hash = window.location.hash.substring(1); // Remove the # symbol
                if (hash === 'register' || hash === 'login') {
                    // Remove active class from all tabs and forms
                    const tabBtns = document.querySelectorAll('.tab-btn');
                    const formWrappers = document.querySelectorAll('.form-wrapper');
                    
                    if (tabBtns.length === 0 || formWrappers.length === 0) {
                        return;
                    }
                    
                    tabBtns.forEach(tab => tab.classList.remove('active'));
                    formWrappers.forEach(wrapper => wrapper.classList.remove('active'));
                    
                    // Activate the correct tab
                    const targetTab = document.querySelector(`[data-tab="${hash}"]`);
                    const targetForm = document.getElementById(hash + '-form');
                    
                    if (targetTab && targetForm) {
                        targetTab.classList.add('active');
                        targetForm.classList.add('active');
                    }
                }
            } catch (error) {
                // Silent error handling
            }
        }
    
    // Handle initial tab on page load
    handleInitialTab();
    
    // Tab switching functionality
    const tabBtns = document.querySelectorAll('.tab-btn');
    const formWrappers = document.querySelectorAll('.form-wrapper');
    
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all tabs and forms
            tabBtns.forEach(tab => tab.classList.remove('active'));
            formWrappers.forEach(wrapper => wrapper.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Show corresponding form
            const targetForm = document.getElementById(targetTab + '-form');
            if (targetForm) {
                targetForm.classList.add('active');
            }
            
            // Update URL hash
            window.location.hash = targetTab;
        });
    });
    
    // Password visibility toggle
    const togglePasswordBtns = document.querySelectorAll('.toggle-password');
    
    togglePasswordBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            const icon = this.querySelector('i');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
    
    // Password strength indicator
    const passwordInput = document.getElementById('registerPassword');
    const strengthFill = document.getElementById('strengthFill');
    const strengthFeedback = document.querySelector('.feedback-text');
    const weakLevel = document.getElementById('weakLevel');
    const mediumLevel = document.getElementById('mediumLevel');
    const strongLevel = document.getElementById('strongLevel');
    
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            updatePasswordStrengthLevels(password);
        });
        
        // Initial state
        updatePasswordStrengthLevels('');
    }
    
    function updatePasswordStrengthLevels(password) {
        if (!password || password.length === 0) {
            // Reset all levels
            if (weakLevel) weakLevel.classList.remove('active');
            if (mediumLevel) mediumLevel.classList.remove('active');
            if (strongLevel) strongLevel.classList.remove('active');
            if (strengthFill) {
                strengthFill.style.width = '0%';
                strengthFill.classList.remove('weak', 'medium', 'strong');
            }
            if (strengthFeedback) {
                strengthFeedback.textContent = 'Enter password to see strength';
            }
            return;
        }
        
        // Calculate strength criteria
        const criteria = {
            length: password.length >= 8,
            lowercase: /[a-z]/.test(password),
            uppercase: /[A-Z]/.test(password),
            numbers: /\d/.test(password),
            special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
        };
        
        const score = Object.values(criteria).filter(Boolean).length;
        
        // Reset all levels
        if (weakLevel) weakLevel.classList.remove('active');
        if (mediumLevel) mediumLevel.classList.remove('active');
        if (strongLevel) strongLevel.classList.remove('active');
        
        // Update levels and bar based on score
        if (strengthFill) {
            strengthFill.classList.remove('weak', 'medium', 'strong');
        }
        
        let strengthLevel = '';
        let feedbackText = '';
        
        if (score <= 2) {
            strengthLevel = 'weak';
            feedbackText = `Weak password. Add ${3-score} more requirements.`;
            if (weakLevel) weakLevel.classList.add('active');
            if (strengthFill) {
                strengthFill.classList.add('weak');
                strengthFill.style.width = '33%';
            }
        } else if (score <= 3) {
            strengthLevel = 'medium';
            feedbackText = `Medium strength. Add ${5-score} more for strong password.`;
            if (weakLevel) weakLevel.classList.add('active');
            if (mediumLevel) mediumLevel.classList.add('active');
            if (strengthFill) {
                strengthFill.classList.add('medium');
                strengthFill.style.width = '66%';
            }
        } else {
            strengthLevel = 'strong';
            feedbackText = 'Strong password! Great job. 🎉';
            if (weakLevel) weakLevel.classList.add('active');
            if (mediumLevel) mediumLevel.classList.add('active');
            if (strongLevel) strongLevel.classList.add('active');
            if (strengthFill) {
                strengthFill.classList.add('strong');
                strengthFill.style.width = '100%';
            }
        }
        
        if (strengthFeedback) {
            strengthFeedback.textContent = feedbackText;
        }
        
        console.log('Password strength:', {
            score: score,
            level: strengthLevel,
            criteria: criteria
        });
    }
    
    // Enhanced form validation
    function validateEmail(email) {
        // More comprehensive email validation
        const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
        return emailRegex.test(email) && email.length <= 254;
    }
    
    function validatePassword(password) {
        // Enhanced password validation
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        
        return {
            isValid: password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers,
            errors: [
                password.length < minLength ? `Password must be at least ${minLength} characters` : null,
                !hasUpperCase ? 'Password must contain at least one uppercase letter' : null,
                !hasLowerCase ? 'Password must contain at least one lowercase letter' : null,
                !hasNumbers ? 'Password must contain at least one number' : null
            ].filter(Boolean)
        };
    }
    
    function validateName(name) {
        const nameRegex = /^[a-zA-Z\s]+$/;
        return {
            isValid: name.length >= 2 && name.length <= 50 && nameRegex.test(name),
            errors: [
                name.length < 2 ? 'Name must be at least 2 characters' : null,
                name.length > 50 ? 'Name must be less than 50 characters' : null,
                !nameRegex.test(name) ? 'Name can only contain letters and spaces' : null
            ].filter(Boolean)
        };
    }
    
    function showError(fieldId, messages) {
        try {
            const errorElement = document.getElementById(fieldId + 'Error');
            if (errorElement) {
                // Handle both string and array of messages
                const errorText = Array.isArray(messages) ? messages.join('. ') : messages;
                errorElement.textContent = errorText;
                errorElement.style.display = 'block';
                errorElement.setAttribute('role', 'alert');
                
                // Add error styling to input
                const inputElement = document.getElementById(fieldId);
                if (inputElement) {
                    inputElement.classList.add('error');
                    inputElement.setAttribute('aria-invalid', 'true');
                    inputElement.setAttribute('aria-describedby', fieldId + 'Error');
                }
            }
        } catch (error) {
            // Silent error handling
        }
    }
    
    function clearError(fieldId) {
        const errorElement = document.getElementById(fieldId + 'Error');
        if (errorElement) {
            errorElement.style.display = 'none';
            errorElement.textContent = '';
            errorElement.removeAttribute('role');
            
            // Remove error styling from input
            const inputElement = document.getElementById(fieldId);
            if (inputElement) {
                inputElement.classList.remove('error');
                inputElement.setAttribute('aria-invalid', 'false');
                inputElement.removeAttribute('aria-describedby');
            }
        }
    }
    
    function clearAllErrors() {
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(element => {
            element.textContent = '';
            element.style.display = 'none';
        });
    }
    
    // Login form submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            clearAllErrors();
            
            const email = document.getElementById('loginEmail').value.trim();
            const password = document.getElementById('loginPassword').value;
            
            let isValid = true;
            
            // Validate email
            if (!email) {
                showError('loginEmail', 'Email is required');
                isValid = false;
            } else if (!validateEmail(email)) {
                showError('loginEmail', 'Please enter a valid email address');
                isValid = false;
            }
            
            // Validate password
            if (!password) {
                showError('loginPassword', 'Password is required');
                isValid = false;
            }
            
            if (isValid) {
                const submitBtn = this.querySelector('button[type="submit"]');
                simulateFormSubmission(submitBtn, 'Signing in...', () => {
                    alert('Login successful! Redirecting to dashboard...');
                    // Here you would typically redirect to the main app
                    console.log('Login data:', { email, password });
                });
            }
        });
    }
    
    // Register form submission
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            clearAllErrors();
            
            const name = document.getElementById('registerName').value.trim();
            const email = document.getElementById('registerEmail').value.trim();
            const password = document.getElementById('registerPassword').value;
            const agreeTerms = document.getElementById('agreeTerms').checked;
            
            let isValid = true;
            
            // Validate name
            if (!name) {
                showError('registerName', 'Full name is required');
                isValid = false;
            } else if (!validateName(name)) {
                showError('registerName', 'Name must be at least 2 characters long');
                isValid = false;
            }
            
            // Validate email
            if (!email) {
                showError('registerEmail', 'Email is required');
                isValid = false;
            } else if (!validateEmail(email)) {
                showError('registerEmail', 'Please enter a valid email address');
                isValid = false;
            }
            
            // Validate password
            if (!password) {
                showError('registerPassword', 'Password is required');
                isValid = false;
            } else {
                const passwordValidation = validatePassword(password);
                if (!passwordValidation.isValid) {
                    showError('registerPassword', passwordValidation.errors);
                    isValid = false;
                }
            }
            
            // Check terms agreement
            if (!agreeTerms) {
                alert('Please agree to the Terms of Service and Privacy Policy');
                isValid = false;
            }
            
            if (isValid) {
                const submitBtn = this.querySelector('button[type="submit"]');
                simulateFormSubmission(submitBtn, 'Creating account...', () => {
                    alert('Registration successful! Welcome to CareerAI!');
                    // Here you would typically redirect to onboarding or dashboard
                    console.log('Registration data:', { name, email, password });
                });
            }
        });
    }
    
    // Continue as Guest functionality
    const guestBtn = document.getElementById('continueAsGuest');
    if (guestBtn) {
        guestBtn.addEventListener('click', function() {
            const confirmGuest = confirm('Continue as guest? You\'ll have limited access to features.');
            if (confirmGuest) {
                simulateFormSubmission(this, 'Starting guest session...', () => {
                    alert('Welcome! You\'re now browsing as a guest.');
                    // Redirect to limited dashboard or main app
                    console.log('Guest access granted');
                });
            }
        });
    }
    
    // Social login buttons
    const socialBtns = document.querySelectorAll('.social-btn');
    socialBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const provider = this.classList.contains('google-btn') ? 'Google' : 
                           this.classList.contains('linkedin-btn') ? 'LinkedIn' : 'Microsoft';
            
            simulateFormSubmission(this, `Connecting to ${provider}...`, () => {
                alert(`${provider} authentication would be handled here.`);
                console.log(`${provider} login initiated`);
            });
        });
    });
    
    // Simulate form submission with loading state
    function simulateFormSubmission(button, loadingText, onComplete) {
        const originalText = button.innerHTML;
        
        // Add loading state
        button.classList.add('loading');
        button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${loadingText}`;
        
        // Simulate API call delay
        setTimeout(() => {
            // Remove loading state
            button.classList.remove('loading');
            button.innerHTML = originalText;
            
            // Execute completion callback
            if (onComplete) {
                onComplete();
            }
        }, 2000);
    }
    
    // Enhanced real-time input validation feedback
    const inputs = document.querySelectorAll('input[type="email"], input[type="password"], input[type="text"]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            const value = this.value.trim();
            
            if (!value) {
                clearError(this.id);
                return;
            }
            
            let validation;
            
            if (this.type === 'email') {
                if (!validateEmail(value)) {
                    showError(this.id, 'Please enter a valid email address');
                } else {
                    clearError(this.id);
                }
            } else if (this.type === 'password') {
                validation = validatePassword(value);
                if (!validation.isValid) {
                    showError(this.id, validation.errors);
                } else {
                    clearError(this.id);
                }
            } else if (this.type === 'text' && (this.id.includes('name') || this.id.includes('Name'))) {
                validation = validateName(value);
                if (!validation.isValid) {
                    showError(this.id, validation.errors);
                } else {
                    clearError(this.id);
                }
            }
        });
        
        // Clear errors on input and provide immediate feedback for passwords
        input.addEventListener('input', function() {
            clearError(this.id);
            
            // Real-time password strength feedback
            if (this.type === 'password' && this.value) {
                const validation = validatePassword(this.value);
                if (validation.errors.length === 0) {
                    this.classList.add('valid');
                } else {
                    this.classList.remove('valid');
                }
            }
        });
        
        // Add ARIA labels for better accessibility
        input.addEventListener('focus', function() {
            if (this.type === 'password') {
                this.setAttribute('aria-describedby', this.id + 'Help ' + this.id + 'Error');
            }
        });
    });
    
    // Add floating animation to shapes
    function animateShapes() {
        const shapes = document.querySelectorAll('.floating-shape');
        shapes.forEach((shape, index) => {
            const randomX = Math.random() * 100;
            const randomY = Math.random() * 100;
            const randomDelay = Math.random() * 5;
            
            shape.style.animationDelay = `${randomDelay}s`;
        });
    }
    
    // Initialize animations
    animateShapes();
    
    // Test password strength functionality
    setTimeout(function() {\n        console.log('Testing password strength functionality...');\n        const testInput = document.getElementById('registerPassword');\n        const testStrengthBar = document.querySelector('.strength-fill');\n        const testStrengthText = document.querySelector('.strength-text');\n        \n        console.log('Test elements found:', {\n            input: !!testInput,\n            bar: !!testStrengthBar,\n            text: !!testStrengthText\n        });\n        \n        if (testInput && testStrengthBar && testStrengthText) {\n            console.log('Password strength system initialized successfully');\n        } else {\n            console.error('Password strength elements not found properly');\n        }\n    }, 1000);\n    
});\n\n// Additional password strength test function\nfunction testPasswordStrength() {\n    const passwordInput = document.getElementById('registerPassword');\n    if (passwordInput) {\n        // Test with a sample password\n        passwordInput.value = 'TestPass123!';\n        passwordInput.dispatchEvent(new Event('input'));\n        console.log('Password strength test completed');\n    }\n}