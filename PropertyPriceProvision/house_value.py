import matplotlib.pyplot as plt
import random
import numpy as np
from cProfile import label
from pandas import *
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
from datetime import datetime

##############################
#        Methods
##############################

def one_hot_encoding(data):
    # integer encode
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(data)
    # binary encode
    onehot_encoder = OneHotEncoder(sparse=False)
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)

    return onehot_encoded

def gradient_descent_LMS(learn_rate, features, y, n_iters):
    wT = np.ones(features.shape[1]) #initialize weight vector
    features_transpose = features.transpose()
    for iter in range(0, n_iters):
       hypothesis = np.dot(features, wT)
       loss = hypothesis - y
       J = np.sum(loss ** 2) / 2  # cost
       #print ("iter %s | J: %.3f" % (iter, J))    
       gradient = np.dot(features_transpose, loss)      
       wT = wT - learn_rate * gradient  # update
    return wT

def get_data_index(data, indeces):
    new_list = []
    for i in indeces:
        new_list.append(data[i])
    return new_list


##############################
#        Main Program
##############################

# Read CSV file
data = read_csv("housing.csv")

# Create a subset for each feature (column)
longitude = np.array(data['longitude'].tolist())
latitude = np.array(data['latitude'].tolist())
housing_median_age = np.array(data['housing_median_age'].tolist())
total_rooms = np.array(data['total_rooms'].tolist())
total_bedrooms = np.array(data['total_bedrooms'].tolist())
population = np.array(data['population'].tolist())
households = np.array(data['households'].tolist())
median_income = np.array(data['median_income'].tolist())
median_house_value = np.array(data['median_house_value'].tolist())
ocean_proximity = np.array(data['ocean_proximity'].tolist())

# Scale arithmetic data to a range of 0 to 1
scaler = MinMaxScaler()
longitude = scaler.fit_transform(longitude.reshape(-1, 1))
latitude = scaler.fit_transform(latitude.reshape(-1, 1))
housing_median_age = scaler.fit_transform(housing_median_age.reshape(-1, 1))
total_rooms = scaler.fit_transform(total_rooms.reshape(-1, 1))
total_bedrooms = scaler.fit_transform(total_bedrooms.reshape(-1, 1))
population = scaler.fit_transform(population.reshape(-1, 1))
households = scaler.fit_transform(households.reshape(-1, 1))
median_income = scaler.fit_transform(median_income.reshape(-1, 1))
median_house_value = scaler.fit_transform(median_house_value.reshape(-1, 1))

# Scale categorical data
ocean_proximity = one_hot_encoding(ocean_proximity)
ocean_proximity = np.array(ocean_proximity)

# Fill missing data with the median value of each feature
imp = SimpleImputer(strategy='mean')
longitude = imp.fit_transform(longitude.reshape(-1, 1))
latitude = imp.fit_transform(latitude.reshape(-1, 1))
housing_median_age = imp.fit_transform(housing_median_age.reshape(-1, 1))
total_rooms = imp.fit_transform(total_rooms.reshape(-1, 1))
total_bedrooms = imp.fit_transform(total_bedrooms.reshape(-1, 1))
population = imp.fit_transform(population.reshape(-1, 1))
households = imp.fit_transform(households.reshape(-1, 1))
median_income = imp.fit_transform(median_income.reshape(-1, 1))
median_house_value = imp.fit_transform(median_house_value.reshape(-1, 1))

# Frequency Histograms for each feature
fig, axs = plt.subplots(2, 5, figsize=(15,5), dpi=100, sharex=True, sharey=True)
fig.suptitle('Frequency Histograms')
axs[0, 0].hist(longitude, bins=50, color='tab:red')
axs[0, 0].set_title('Longitude')
axs[0, 1].hist(latitude, bins=50, color='tab:blue')
axs[0, 1].set_title('Latitude')
axs[0, 2].hist(housing_median_age, bins=50, color='tab:orange')
axs[0, 2].set_title('Housing Median Age')
axs[0, 3].hist(total_rooms, bins=50, color='tab:green')
axs[0, 3].set_title('Total Rooms')
axs[0, 4].hist(total_bedrooms, bins=50, color='tab:purple')
axs[0, 4].set_title('Total_bedrooms')
axs[1, 0].hist(population, bins=50, color='tab:cyan')
axs[1, 0].set_title('Population')
axs[1, 1].hist(households, bins=50, color='tab:olive')
axs[1, 1].set_title('Households')
axs[1, 2].hist(median_income, bins=50, color='tab:brown')
axs[1, 2].set_title('Median Income')
axs[1, 3].hist(median_house_value, bins=50, color='tab:grey')
axs[1, 3].set_title('Median House Value')
plt.show()

# 2D Graphs
fig2, axs2 = plt.subplots(1, 3, figsize=(15,5), dpi=100)
fig2.suptitle('2D Graphs')

axs2[0].plot(total_bedrooms, color='tab:purple', label='Total Bedrooms')
axs2[0].plot(population, color='tab:cyan', label='Population')
axs2[0].legend(loc='upper left')

axs2[1].plot(median_income, color='tab:brown', label='Median Income')
axs2[1].plot(households, color='tab:olive', label='Households')
axs2[1].plot(population, color='tab:cyan', label='Population')
axs2[1].legend(loc='upper left')

axs2[2].plot(median_house_value, color='tab:grey', label='Median House Value')
axs2[2].plot(median_income, color='tab:brown', label='Median Income')
axs2[2].plot(total_bedrooms, color='tab:purple', label='Total Bedrooms')
axs2[2].plot(population, color='tab:cyan', label='Population')
axs2[2].legend(loc='upper left')
plt.show()

#-----------------------DATA TRAINNING-----------------------
# Get trainning data
random.seed(str(datetime.now()))
num_of_train_indices = 100
train_indices = random.sample(range(2, len(longitude)), num_of_train_indices) # Generate random indices
train_indices = list(dict.fromkeys(train_indices)) # Remove doubles indices

train_longitude = np.array(get_data_index(longitude, train_indices))
train_latitude =  np.array(get_data_index(latitude, train_indices))
train_housing_median_age =  np.array(get_data_index(housing_median_age, train_indices))
train_total_rooms =  np.array(get_data_index(total_rooms, train_indices))
train_total_bedrooms =  np.array(get_data_index(total_bedrooms, train_indices))
train_population =  np.array(get_data_index(population, train_indices))
train_households =  np.array(get_data_index(households, train_indices))
train_median_income =  np.array(get_data_index(median_income, train_indices))
train_median_house_value =  np.array(get_data_index(median_house_value, train_indices))

train_longitude = np.concatenate(train_longitude, axis=0)
train_latitude = np.concatenate(train_latitude, axis=0)
train_housing_median_age = np.concatenate(train_housing_median_age, axis=0)
train_total_rooms = np.concatenate(train_total_rooms, axis=0)
train_total_bedrooms = np.concatenate(train_total_bedrooms, axis=0)
train_population = np.concatenate(train_population, axis=0)
train_households = np.concatenate(train_households, axis=0)
train_median_income = np.concatenate(train_median_income, axis=0)
train_median_house_value = np.concatenate(train_median_house_value, axis=0)

train_features = np.stack((train_longitude, train_latitude, train_housing_median_age, train_total_rooms, 
train_total_bedrooms, train_population, train_households, train_median_income), axis=1)
# LMS algorithm
m, n = np.shape(train_features)
train_features = np.c_[ np.ones(m), train_features] # insert dummy column

W1 = gradient_descent_LMS(0.01, train_features, train_median_house_value, 1000)
print(W1)

#-----------------------DATA TESTING-----------------------
num_of_test_indices = 10
test_indices = random.sample(range(2, len(longitude)), num_of_test_indices) # Generate random indices
test_indices = list(dict.fromkeys(test_indices)) # Remove doubles indices
for y in range(0, num_of_test_indices):
    i = test_indices[y]
    median_house_value_predict = W1[0] + W1[1]*longitude[i] + W1[2]*latitude[i] + W1[3]*housing_median_age[i] + W1[4]*total_rooms[i]
    + W1[5]*total_bedrooms[i] + W1[6]*population[i] + W1[7]*households[i] + W1[8]*median_income[i]
    print ("Predict Value %F | Real Value: %F" % (median_house_value_predict, median_house_value[i]))   
    print(i)
