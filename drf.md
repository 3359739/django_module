# drf源码理解

```python
path('index/<int:pk>',views.qiniu_img.as_view())
 
views.qiniu_img.as_view()会去qiniu_img找到对应的方法而qiniu_img本身没有这个类会去其父类找到as_view()
as_view()里面实例化了qiniu_img返回一个self.dispatch
进入as_views(而as_views返回的是类内部的一个view方法)
view里面返回一个内部方法self.dispatch->(def dispatch(self, request, *args, **kwargs))

def dispatch(self, request, *args, **kwargs):
    if request.method.lower() in self.http_method_names:
        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        这里是查找里面是否有对应的方法
    else:
        handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
        这里执行对应的方法体
总得来说是
向去qiniu_img中查找对as_view()->
as_view()->view()->dispatch()->handler()
```









## GPT回答

1. **调用 `views.qiniu_img.as_view()`**
   - 这一步会去 `qiniu_img` 类找到 `as_view()` 方法。如果 `qiniu_img` 本身没有这个方法，它会去其父类找到 `as_view()` 方法。
2. **`as_view()` 方法**
   - `as_view()` 方法是一个类方法（通常是类视图中的类方法），它负责实例化该类并返回一个视图函数。这通常是通过返回 `cls().view()` 实现的。
3. **`view` 方法**
   - `view` 方法通常是返回一个实际处理 HTTP 请求的函数。在类视图中，这个方法通常是返回一个内部的 `dispatch` 方法。
4. **`dispatch` 方法**
   - `dispatch` 方法是类视图中处理 HTTP 请求的核心方法。它根据请求的方法（GET、POST、PUT 等）来选择合适的处理函数。
   - 具体来说，`dispatch` 方法会检查 `request.method.lower()` 是否在 `self.http_method_names` 中。如果在，它会使用 `getattr` 找到对应的方法（例如 `get`、`post` 等）；如果不在，它会调用 `self.http_method_not_allowed` 方法。
5. **调用处理函数**
   - 最终，`dispatch` 方法会调用找到的处理函数并返回其结果。

总的来说，流程如下：

1. **查找 `as_view()`**：在 `qiniu_img` 类或其父类中查找 `as_view()` 方法。
2. **调用 `as_view()`**：`as_view()` 方法实例化 `qiniu_img` 类并返回一个视图函数。
3. **视图函数调用 `dispatch`**：视图函数调用类的 `dispatch` 方法来处理请求。
4. **`dispatch` 方法选择处理函数**：`dispatch` 方法根据请求的方法选择合适的处理函数。
5. **调用处理函数**：调用处理函数并返回结果。





# 认证组件源码解析(authentication)

```python

drf的认证流程
进入到dispatch方法中重新封装了request然后传给了 self.initial(request, *args, **kwargs)
self.initial(request, *args, **kwargs) 方法中调用了 self.perform_authentication(request) 方法
self.perform_authentication(request) 方法中调用了 内容 request.user 方法
而这request方法是封装后的request的所以这里调用会去到新reques找到user
这个user是一个 
@property(这是方法转换成属性：可以通过getter和setter方法控制属性的访问和修改。这有助于封装类的内部实现，防止外部直接访问和修改属性。)
def user(self):
    if not hasattr(self, '_user'):这里先从实例类进行找没有找到则进入到判断里面
        with wrap_attributeerrors():
            self._authenticate()会到这里来
        return self._user
def _authenticate(self):
        for authenticator in self.authenticators://这里是我们的认证类
            try:
                user_auth_tuple = authenticator.authenticate(self)//调用我们重新的authenticate方法进行赋值
            except exceptions.APIException:
                self._not_authenticated()
                raise
        if user_auth_tuple is not None:
                self._authenticator = authenticator保存我们认证器
                self.user, self.auth = user_auth_tuple把认证方法返回的内容赋值
                return

```

## GTP回答：

### DRF 认证流程详解

1. **进入 `dispatch` 方法**：

   - 当DRF处理一个请求时，它首先调用视图的 `dispatch` 方法。`dispatch` 方法负责将请求方法（如 GET、POST 等）分派给相应的处理器方法（如 `get`、`post` 等）。

2. **重新封装请求**：

   - 在 `dispatch` 方法中，DRF 会重新封装请求对象，将其转换为一个REST framework的 `Request` 对象，并调用 `self.initial(request, *args, **kwargs)` 方法。

3. **调用 `self.initial` 方法**：

   - `self.initial(request, *args, **kwargs)` 方法中，DRF执行了一些初始化操作，其中包括调用 `self.perform_authentication(request)` 方法来处理认证。

4. **执行认证**：

   - `self.perform_authentication(request)` 方法调用 `request.user`，以确保请求已被认证。
   - `request.user` 是一个属性，使用了 `@property` 装饰器。

5. **`request.user` 属性**：

   - 当访问 

     ```
     request.user
     ```

      时，

     ```
     Request
     ```

      对象的 

     ```
     user
     ```

      属性方法被调用：

     ```
     python复制代码@property
     def user(self):
         if not hasattr(self, '_user'):
             with wrap_attributeerrors():
                 self._authenticate()
         return self._user
     ```

   - `user` 属性方法首先检查 `self` 实例是否有 `_user` 属性。如果没有，它将调用 `self._authenticate()` 方法进行认证。

6. **`_authenticate` 方法**：

   - ```
     self._authenticate()
     ```

      方法负责遍历所有的认证器并尝试认证请求：

     ```
     python复制代码def _authenticate(self):
         for authenticator in self.authenticators:
             try:
                 user_auth_tuple = authenticator.authenticate(self)
             except exceptions.APIException:
                 self._not_authenticated()
                 raise
     
             if user_auth_tuple is not None:
                 self._authenticator = authenticator
                 self.user, self.auth = user_auth_tuple
                 return
     
         self._not_authenticated()
     ```

   - 在这个方法中，DRF遍历 `self.authenticators` 列表中的每个认证器，并调用它们的 `authenticate(self)` 方法。

   - 如果认证成功，`authenticate` 方法返回一个包含用户和认证信息的元组（`user_auth_tuple`）。

   - 认证成功后，`self._authenticator` 被设置为成功认证的认证器，`self.user` 和 `self.auth` 被设置为认证返回的用户和认证信息。

7. **处理认证异常**：

   - 如果 `authenticate` 方法抛出 `APIException` 异常，`self._not_authenticated()` 方法被调用，并重新抛出异常。
   - `self._not_authenticated()` 方法用于清理认证相关的属性。

8. **返回用户**：

   - 经过 `_authenticate` 方法的处理，`user` 属性方法返回认证后的用户对象。

### 整理后的完整流程

1. 请求进入视图的 `dispatch` 方法。
2. `dispatch` 方法重新封装请求，并调用 `self.initial(request, *args, **kwargs)`。
3. `self.initial` 方法中调用 `self.perform_authentication(request)`。
4. `self.perform_authentication` 方法访问 `request.user`。
5. `request.user` 属性方法检查 `_user` 属性，如果不存在则调用 `_authenticate` 方法。
6. `_authenticate` 方法遍历认证器，尝试认证请求。
7. 认证成功后，设置 `_authenticator`、`user` 和 `auth` 属性。
8. 如果认证失败，抛出 `APIException` 异常。
9. `user` 属性方法返回认证后的用户对象。



# 权限组件permission

```python
"""
权限类from rest_framework.permissions import BasePermission
先进入到self.dispatch()然后进行self.initial(request, *args, **kwargs)
self.perform_authentication(request)进行认证之后会走到
self.check_permissions(request)进入到权限认证
check_permissions分析：
   1.遍历权限类，进行权限认证：self.get_permissions()先去本类中找权限类，如果没有再到父类中找在类中定义permission_classes=[]方法会覆盖调setting里面的配置
   def check_permissions(self, request):
        for permission in self.get_permissions():这里拿自定义取权限类然后进行遍历
            if not permission.has_permission(request, self):
            调用类里面的has_permission方法要是为false就会不在进行遍历调用permission_denied方法进行返回不满足权限
             这里会遍历执行自定义的权限类，要是有一个权限类不满足权限就会跳出循环
                self.permission_denied(
                    request,
                    message=getattr(permission, 'message', None),
                    code=getattr(permission, 'code', None)
                )
执行先后dispatch-》initial-》perform_authentication-》check_permissions
"""
```



## 重写check_permissions方法实现or

```python
def check_permissions(self, request):
       substance=False
       for permission in self.get_permissions():#获得所有类进行遍历
            if permission.has_permission(request, self):#然后进行调用
                self.substance=True#要是有一个类返回True则 substance为True表有权限登录
                return
       if not substance:
            self.permission_denied(request,message=getattr(permission, 'message', None),code=getattr(permission, 'code', None))
```

## GTP回答

在 Django REST Framework 中，权限组件用于控制用户是否有权限访问特定的 API 视图。权限组件通常基于用户的身份、请求的内容等因素进行判断。下面是关于权限组件的一些详细信息：

### 权限组件的作用

1. **控制访问权限**：权限组件决定了谁可以访问 API 的哪些部分，以及能够执行什么样的操作。
2. **保护敏感数据**：通过限制对敏感数据的访问，权限组件可以帮助保护用户隐私和保密信息。

### DRF 中的权限组件

在 Django REST Framework 中，权限组件通常继承自 `rest_framework.permissions.BasePermission` 类，并实现其中的 `has_permission` 或 `has_object_permission` 方法。这些方法用于检查用户是否具有执行特定操作的权限。

### 常见的权限组件

1. **IsAuthenticated**：确保用户已经通过身份验证。
2. **AllowAny**：允许任何用户访问视图，即不需要身份验证。
3. **IsAdminUser**：仅允许管理员用户访问视图。
4. **IsAuthenticatedOrReadOnly**：允许已验证用户执行写操作，但允许未验证用户执行只读操作。
5. **Custom permissions**：开发人员可以根据应用程序的需求定义自己的自定义权限。

### 权限配置方式

1. **全局配置**：在 Django REST Framework 的设置中配置全局默认权限类，适用于整个应用程序。
2. **视图级配置**：在 API 视图中指定特定的权限类，以覆盖全局设置，并使得某个视图可以使用不同的权限规则。
3. **动态配置**：有时需要根据请求中的内容动态地选择权限类，这可以通过编写自定义的权限类或者使用装饰器来实现。

### 权限检查流程

1. **进入视图**：请求到达 API 视图。
2. **调用权限检查方法**：在视图中调用权限检查方法（通常是 `check_permissions` 方法）。
3. **遍历权限类**：遍历所有配置的权限类。
4. **执行权限检查**：对每个权限类调用 `has_permission` 方法，检查是否具有权限。
5. **处理权限不足**：如果有任何一个权限类返回 `False`，则触发权限不足的处理机制，通常是返回相应的错误响应。

### 总结

权限组件是 Django REST Framework 中非常重要的一部分，它控制了用户对 API 的访问权限。了解权限组件的工作原理和常见用法对于开发安全可靠的 API 非常重要。

