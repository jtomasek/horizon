/* Namespace for core functionality related to Membership Workflow Step. */
horizon.membership = {

  compile_modal_template: function() {
    var modal = $('#modal_wrapper .modal-body');
    var html = modal.html();
    var element = angular.element('body');
    var compiler = element.injector().get('$compile');
    var scope = element.scope();
    var compiledTemplate = compiler(html)(scope);
    angular.element('#modal_wrapper .modal-body').html(compiledTemplate);
  },

  /*
   * Calls set-up functions upon loading the workflow.
   **/
  workflow_init: function(modal, step_slug, step_id) {
    // fix the dropdown menu overflow issues
    $(".tab-content, .workflow").addClass("dropdown_fix");

    $(modal).find('form').each( function () {
        var $form = $(this);

        // Do nothing if this isn't a membership modal
        if ($form.find('div.' + step_slug + '_membership').length === 0) {
           return; // continue
        }

        // prevent filter inputs from submitting form on 'enter'
        $form.find('.' + step_slug + '_membership').keydown(function(event){
            if(event.keyCode == 13) {
              event.preventDefault();
              return false;
            }
        });

    });

    horizon.membership.compile_modal_template();

  }
};
