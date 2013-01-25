Exceptions
----------

exceptions_with_attributes.py
+++++++++++++++++++++++++++++

A quick test of creating exceptions with custom attributes. The motivation
came about in a Django project. A function was calling a calling a Manager
method which raised a custom already-exists exception. In the except clause
of the calling function, the same query was performed again to log the ID
of the pre-existing object. If the exception carried to existing object with
it, there would be no need for the query to be done twice.
