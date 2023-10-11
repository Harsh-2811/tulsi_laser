from customers.forms import CustomerForm
from customers.models import Customer
from django.shortcuts import redirect
class CustomerInline():
    form_class = CustomerForm
    model = Customer
    template_name = "add_customer.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.customer = self.object
                formset.save()
        return redirect('customers')

    def formset_machines_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        machines = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for machine in machines:
            machine.customer = self.object
            machine.save()