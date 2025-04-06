
window.addEventListener('load', function() {
  const summaryButton = document.querySelector('.tab-button:nth-child(2)'); // Assuming "Summary" is the second button
  if (summaryButton) {
    summaryButton.click(); // Simulates a click on the "Summary" button
  }
});

function showTab(tabId, clickedButton) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active-tab'));
  
    // Show the selected tab
    const selectedTab = document.getElementById(tabId);
    selectedTab.classList.add('active-tab');

    // Remove active class from all tab buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Add active class to the selected tab button
    clickedButton.classList.add('active');
  }
  