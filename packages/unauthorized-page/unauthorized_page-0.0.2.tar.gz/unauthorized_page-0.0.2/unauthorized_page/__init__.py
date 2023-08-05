
def unauthenticated_user(redirect, redirect_page):
  def view_function(view_func):
    def wrapper_func(request, *args, **kwargs):
      print(request.user.is_authenticated)
      if request.user.is_authenticated:
        return redirect(redirect_page)
      else:
        return view_func(request, *args, **kwargs)

    return wrapper_func
  return view_function