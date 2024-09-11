New Task For Odoo version 15 ! 
This Task contains Many Of Important Codes And Some Useful Customization for exsisting module and module From Scratch, 
I Hope It Will Be Useful For Beginner odoo Developers !........
The Task :
Small brief for project business cycle:
Our client(Wooden tools store) wants to create a system to allow him to enter
customer data and their orders from the store.
Create new Model Called Technical Order with a new menuitem called "Orders"
placed under Store Orders menu
Form fields:
-Sequence (TO0001,TO0002,TO0003,...,etc)
-Request name (Char and mandatory)
-Requested by (many2one from res.users, mandatory and takes by default active
user)
-Start Date (date field with today's date as default)
-End Date (date field)
-Rejection Reason (Text field, invisible except in reject state, readonly)
- orderlines One to Many field from (Technical Order Line) with fields:
1- product_id (many to one field from product.product, mandatory)
2- Description (Char field takes name of selected product)
3- Quantity (field Float by default=1)
4- Price (field Float, readonly field, reads from products lst price)
5- Total (readonly field, it's value comes from quantity * price)
-Total Price (Float field, Sum of orderlines' total)
-status selection field with states (draft, to be approved, approve, reject, cancel),
show as statusbar on form, not clickable.
Buttons:
-In draft state show buttons "Submit for Approval" and "Cancel"
-In Submit for Approval state show buttons "Approve" and "Reject"
-In Cancel state show button "Reset to draft"
Workflow and buttons actions:
-If pressed Submit for Approval, Technical order state changes to "to be approved"
-If pressed Cancel, Technical order state changes to "cancel"
-If pressed Approve, Send email to all users in sale manager group saying
"Technical Order (x) has been approved" where x is the name of the technical order.
-If pressed Reject, New Wizard will pop up with field Rejection Reason (Text field
and mandatory) and confirm and cancel btn
-wizard confirm button, set's the technical order rejection reason field with the value
entered in the wizard
-cancel closes the wizard states.Print out:
Create a Qweb report, that will print all information on the page (all fields on
technical.order and table with lines)
In Model Technical Order, apply the following:
- in Approved state, add a new button called "Create SO"
- if pressed this button a new draft SO "sale.order" (model already exists, you have
to install Sales module), will be created with the same values as the TO.
- Hide "create SO" btn from the TO, if all quantities were taken in Confirmed SOs
- Show a smart button in the TO called "Technical Orders" with count (to show the
related no. of created sale orders), if smart button pressed, a tree view will be shown
for the related created SOs, this smart button will be shown in approved state.
