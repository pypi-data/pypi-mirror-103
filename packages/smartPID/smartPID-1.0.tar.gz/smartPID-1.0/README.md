# The smartPID Library

### 1. Background
This library contains three kinds of PID controller algorithms, which are position PID controller, incremental PID controller and single neural PID controller. According to different scenarios, different types of controller algorithms can be called after loading the library.
### 2. About the author
This library is compiled by Qi Zhu from the People's Republic of China.
## 3. Environment
This library is written in Python 3.7.
## 4. Dependent Libraries
This library needs to use the *time* library, so before using this library, you need to make sure that your environment already contains the *time* library.
## 5. How to use the library
The first step is to download the library.
```ruby  
pip install smartPID
```
Then load the library where you need it.
```ruby  
import smartPID
```
### 5.1 Position PID Controller
When you need to call the position PID controller, you can refer to the following code.The variable *input_signal* here refers to the feedback value of the measurement.
```ruby  
smartPID.position(input_signal)
```
You can use the following methods to set the PID parameters of the controller. (When we assume P = 0.2, I=0.5, D=0.1)
```ruby  
smartPID.set_PID(0.2,0.5,0.1)
```
You can use the following methods to set the setpoint of the PID controller. (When we assume setpoint = 5)
```ruby  
smartPID.set_set_point(5)
```
You can use the following methods to set the sampletime of the PID controller. (When we assume sampletime = 0.01)
```ruby  
smartPID.set_sampletime(0.01)
```
You can use the following methods to display the parameter of the PID controller.
```ruby  
smartPID.display_PIDvalue()
```
### 5.2 Incremental PID Controller
When you need to call the incremental PID controller, you can refer to the following code.The variable *input_signal* here refers to the feedback value of the measurement.
```ruby  
smartPID.incremental(input_signal)
```
You can use the following methods to set the PID parameters of the controller. (When we assume P = 0.2, I=0.5, D=0.1)
```ruby  
smartPID.set_PID(0.2,0.5,0.1)
```
You can use the following methods to set the setpoint of the PID controller. (When we assume setpoint = 5)
```ruby  
smartPID.set_set_point(5)
```
You can use the following methods to set the sampletime of the PID controller. (When we assume sampletime = 0.01)
```ruby  
smartPID.set_sampletime(0.01)
```
You can use the following methods to display the parameter of the PID controller.
```ruby  
smartPID.display_PIDvalue()
```
### 5.3 Single Neural PID Controller
When you need to call the single neural PID controller, you can refer to the following code.The variable *input_signal* here refers to the feedback value of the measurement.
```ruby  
smartPID.SNPID(input_signal)
```
You can use the following methods to set the learning rate of the whole single neural PID controller and each link. (When we assume the whole single neural PID learning rate is 0.03, the P link learning rate is 0.4,  the I link learning rate is 0.2, the D link learning rate is 0.1)
```ruby  
smartPID.set_SNPID_LR(0.03,0.4,0.2,0.1)
```
You can use the following methods to set the initial values of the P link, I link and D link. (When we assume the initial value of the P link is 1.5, the initial value of the I link is 0.3, the initial value of the D link is 0.1)
```ruby  
smartPID.set_SNPID_IW(1.5,0.3,0.1)
```
You can use the following methods to set the setpoint of the single neural PID controller. (When we assume setpoint = 5)
```ruby  
smartPID.set_set_point(5)
```
You can use the following methods to set the sampletime of the single neural PID controller. (When we assume sampletime = 0.01)
```ruby  
smartPID.set_sampletime(0.01)
```
You can use the following methods to display the parameter of the single neural PID controller.
```ruby  
smartPID.display_SNPIDvalue()
```
### 5.4 Default parameters for the library
The default parameters of the position PID controller are as follows:
```ruby  
P=0.2

I=0.0

D=0.0

sampletime=0.01
```
The default parameters of the incremental PID controller are as follows:
```ruby  
P=0.2

I=0.0

D=0.0

sampletime=0.01
```
The default parameters of the single neural PID controller are as follows:
```ruby  
the whole single neural PID learning rate is 0.03

the P link learning rate is 0.1

the I link learning rate is 0.1

the D link learning rate is 0.1

the initial value of the P link is 0.1

the initial value of the I link is 0.1

the initial value of the D link is 0.1

sampletime=0.01
```