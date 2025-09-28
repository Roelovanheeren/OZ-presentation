document.getElementById('research-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Show loading state
    const submitBtn = document.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Generating Report...';
    submitBtn.disabled = true;
    
    // Collect form data
    const formData = new FormData(this);
    const data = {};
    
    // Handle regular form fields
    for (let [key, value] of formData.entries()) {
        if (key === 'key_priorities') {
            if (!data[key]) data[key] = [];
            data[key].push(value);
        } else {
            data[key] = value;
        }
    }
    
    // Convert priorities array to string if it exists
    if (data.key_priorities) {
        data.key_priorities = data.key_priorities.join(', ');
    }
    
    console.log('Form data being sent:', data);
    
    try {
        // Your Relevance webhook URL - UPDATED 2024
        const webhookURL = 'https://api-f1db6c.stack.tryrelevance.com/latest/agents/hooks/custom-trigger/231d3908-fd4e-4835-8cc5-5a8fc4fcb449/b7b4bf17-2e14-4fa6-833b-7123e37bb6e2';
        
        const response = await fetch(webhookURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        console.log('Response status:', response.status);
        
        if (response.ok) {
            // Success message
            document.querySelector('.container').innerHTML = `
                <div style="text-align: center; padding: 60px 20px;">
                    <h2 style="color: #2c3e50; margin-bottom: 20px;">Thank You!</h2>
                    <p style="font-size: 18px; margin-bottom: 15px;">Your real estate market research report is being generated.</p>
                    <p style="color: #666;">You'll receive it at <strong>${data.email}</strong> within 20 minutes.</p>
                    <p style="color: #666; margin-top: 20px;">Don't forget to check your spam folder!</p>
                </div>
            `;
        } else {
            const errorText = await response.text();
            console.error('Response error:', errorText);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`Something went wrong: ${error.message}. Please try again or contact support.`);
        
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
});
// Test push Sun Sep 28 22:42:27 WITA 2025
