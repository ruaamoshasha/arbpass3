document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const inputWord = document.getElementById('inputWord');
    const submitBtn = document.getElementById('submitBtn');
    const resetBtn = document.getElementById('resetBtn');
    const resultArabic = document.getElementById('resultArabic');
    const resultEnglish = document.getElementById('resultEnglish');
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    // Event Listeners
    submitBtn.addEventListener('click', submitWord);
    inputWord.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            submitWord();
        }
    });
    
    resetBtn.addEventListener('click', function() {
        inputWord.value = '';
        resultArabic.textContent = 'النتيجة ستظهر هنا...';
        resultEnglish.textContent = 'النتيجة ستظهر هنا...';
        inputWord.focus();
    });
    
    // Copy to clipboard functionality
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const target = document.getElementById(this.getAttribute('data-target'));
            copyToClipboard(target.textContent);
            
            // Change button text temporarily
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="bi bi-check-lg"></i> تم النسخ';
            
            setTimeout(() => {
                this.innerHTML = originalText;
            }, 2000);
        });
    });
    
    // Functions
    async function submitWord() {
        const input = inputWord.value.trim();
        
        if (!input) {
            showError('يرجى إدخال نص للتحويل');
            return;
        }
        
        try {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> جاري التحويل...';
            
            const response = await fetch("/submit", {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ input })
            });
            
            if (!response.ok) {
                throw new Error('فشل في الاتصال بالخادم');
            }
            
            const data = await response.json();
            
            if (data.error) {
                showError(data.error);
                return;
            }
            
            // Display results with animation
            displayResult(resultArabic, data.result_arabic);
            displayResult(resultEnglish, data.result_english);
            
        } catch (error) {
            showError(error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="bi bi-arrow-right-circle"></i> تحويل';
        }
    }
    
    function displayResult(element, text) {
        element.textContent = text;
        element.parentElement.classList.remove('fadeIn');
        void element.parentElement.offsetWidth; // Trigger reflow
        element.parentElement.classList.add('fadeIn');
    }
    
    function showError(message) {
        // Create a Bootstrap alert for errors
        const alertContainer = document.createElement('div');
        alertContainer.className = 'alert alert-danger alert-dismissible fade show';
        alertContainer.role = 'alert';
        alertContainer.innerHTML = `
            <i class="bi bi-exclamation-triangle-fill"></i> <strong>خطأ:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        // Insert at the top of the card body
        const cardBody = document.querySelector('.card-body');
        cardBody.insertBefore(alertContainer, cardBody.firstChild);
        
        // Auto dismiss after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertContainer);
            bsAlert.close();
        }, 5000);
    }
    
    function copyToClipboard(text) {
        // Create temporary element
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        
        // Select and copy
        textarea.select();
        document.execCommand('copy');
        
        // Remove temporary element
        document.body.removeChild(textarea);
    }
});