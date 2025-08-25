// Nuclear option: Fix Agent 3 black bar with JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎯 Agent 3 Fix Script Loaded');
    
    function fixAgent3Color() {
        try {
            // Find all chart containers
            const chartContainers = document.querySelectorAll('.chart-container');
            
            chartContainers.forEach(container => {
                // Look for Agent Performance charts (wide cards)
                const parentCard = container.closest('.wide-card');
                if (!parentCard) return;
                
                // Find SVG elements
                const svgElements = container.querySelectorAll('svg');
                svgElements.forEach(svg => {
                    // Find all bars/rectangles that might be Agent 3
                    const paths = svg.querySelectorAll('path');
                    const rects = svg.querySelectorAll('rect');
                    
                    // Fix any black fills
                    [...paths, ...rects].forEach((element, index) => {
                        const fill = element.getAttribute('fill');
                        if (fill === '#000000' || fill === 'black' || fill === 'rgb(0,0,0)') {
                            console.log(`🔧 Fixed black element at index ${index}:`, element);
                            element.setAttribute('fill', '#00FF88');
                            element.setAttribute('stroke', '#23263A');
                            element.setAttribute('stroke-width', '2');
                        }
                        
                        // Special handling for position 4 (Agent 3 position)
                        if (index === 4) {
                            const currentFill = element.getAttribute('fill');
                            if (currentFill !== '#00FF88') {
                                console.log(`🎯 AGENT 3 FIX: Changed color from ${currentFill} to #00FF88`);
                                element.setAttribute('fill', '#00FF88');
                                element.setAttribute('stroke', '#23263A');
                                element.setAttribute('stroke-width', '2');
                            }
                        }
                    });
                    
                    // Also check for hover elements
                    const hoverElements = svg.querySelectorAll('[data-unformatted*="Agent 3"]');
                    hoverElements.forEach(element => {
                        const parentBar = element.closest('g');
                        if (parentBar) {
                            const barElement = parentBar.querySelector('path, rect');
                            if (barElement) {
                                console.log('🎯 Fixed Agent 3 via hover element');
                                barElement.setAttribute('fill', '#00FF88');
                            }
                        }
                    });
                });
            });
        } catch (error) {
            console.log('⚠️ Agent 3 fix error:', error);
        }
    }
    
    // Run fix immediately
    fixAgent3Color();
    
    // Run fix after a delay to catch dynamic content
    setTimeout(fixAgent3Color, 1000);
    setTimeout(fixAgent3Color, 3000);
    
    // Run fix when DOM changes (for dynamic updates)
    const observer = new MutationObserver(fixAgent3Color);
    observer.observe(document.body, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['fill']
    });
    
    console.log('🎯 Agent 3 Fix Script Active - Monitoring for changes');
});

console.log('🎯 Agent 3 JavaScript Fix Loaded');
