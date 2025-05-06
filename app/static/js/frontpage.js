document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('darkModeToggle');
    toggleButton.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        this.textContent = document.body.classList.contains('dark-mode') ? '☀️ Light Mode' : '🌙 Dark Mode';
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const cardContainers = document.querySelectorAll('.card-container');
    
    cardContainers.forEach(container => {
        const card = container.querySelector('.card');
        
        // Mouse move tilt effect with depth
        container.addEventListener('mousemove', (e) => {
            const rect = container.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = container.offsetWidth / 2;
            const centerY = container.offsetHeight / 2;
            
            const xAxis = (centerX - x) / 15;
            const yAxis = (centerY - y) / 15;
            
            card.style.transform = `rotateY(${-xAxis}deg) rotateX(${yAxis}deg)`;
            
            // Subtle shadow movement
            const shadowX = xAxis * 2;
            const shadowY = yAxis * 2;
            const shadowBlur = 30 + Math.abs(xAxis) * 2;

            // Check if dark mode is enabled and change shadow accordingly
            const isDarkMode = document.body.classList.contains('dark-mode');
            const shadowColor = isDarkMode ? 'rgba(255, 255, 255, 0.4)' : 'rgba(0, 0, 0, 0.3)';
            
            // Set the shadow color based on dark/light mode
            card.style.boxShadow = `${shadowX}px ${shadowY}px ${shadowBlur}px ${shadowColor}`;
        });
        
        // Reset on mouse leave
        container.addEventListener('mouseleave', () => {
            card.style.transform = 'rotateY(0) rotateX(0)';
            card.style.boxShadow = '0 15px 40px rgba(0,0,0,0.3)';
        });
        
        // Click effect with bounce
        card.addEventListener('click', function() {
            this.classList.add('clicked');
            setTimeout(() => {
                this.classList.remove('clicked');
            }, 500);
        });
        
        // Floating animation
        function floatAnimation() {
            if (!container.matches(':hover')) {
                const time = Date.now() * 0.001;
                const y = Math.sin(time * 0.5) * 3;
                const x = Math.cos(time * 0.3) * 2;
                card.style.transform = `translateY(${y}px) translateX(${x}px)`;
            }
            requestAnimationFrame(floatAnimation);
        }
        
        floatAnimation();
    });
});
