import $ from 'jquery';
import { ajaxEnableCSRF, setStatusMessage } from 'common/utils/';
import 'common/datetimepicker';
import 'font-awesome/css/font-awesome.css';

ajaxEnableCSRF($);

$('.dtp').datetimepicker({
    locale: 'nb',
    format: 'YYYY-MM-DD HH:mm:ss',
});

$(document).ready(() => {
  // Generic javascript to enable interactive tabs that do not require page reload
  const switchTab = (newActiveTab) => {
    if ($('#meetapp-tabs').length) {
      const tabElement = $('#meetapp-tabs').find(`[data-section="${newActiveTab}"]`);
      if (tabElement.length) {
        // Hide sections
        $('#tab-content section').hide();
        // Unmark currently active tab
        $('#meetapp-tabs').find('li.active').removeClass('active');
        // Update the active tab to the clicked tab and show that section
        tabElement.parent().addClass('active');
        $(`#${newActiveTab}`).show();
        // Update URL
        window.history.pushState({}, document.title, $(tabElement).attr('href'));
      }
    }
  };

  // Hide all other tabs and show the active one when the page loads
  if ($('#meetapp-tabs').length) {
    // Hide all sections
    $('#tab-content section').hide();
    // Find the currently active tab and show it
    const activeTab = $('#meetapp-tabs').find('li.active a').data('section');
    $(`#${activeTab}`).show();

    // Set up the tabs to show/hide when clicked
    $('#meetapp-tabs').on('click', 'a', function tabClick(e) {
      e.preventDefault();
      const newActiveTab = $(this).data('section');
      switchTab(newActiveTab);
    });
  }

  // Fix for tabs when going 'back' in the browser history
  window.addEventListener('popstate', () => {
    // If you can figure out how to do this properly, be my guest.
  });
});
