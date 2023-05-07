from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
from django.core.cache import cache
from recommendation_system_backend.ContentBasedRS import ContentBasedRS
from recommendation_system_backend.HybridBasedRS import Hybrid_rec
from recommendation_system_backend.ContentBased_locRS import ContentBased_locRS
from recommendation_system_backend.TopPlacesRS import get_recommendations
from recommendation_system_backend.Feedback import feedback
from datetime import date

def submitReview(request):
	# Get the businessId, userId, review and rating from the GET request
	businessId = request.GET.get('businessId', None)
	userId = request.GET.get('userId', None)
	review = request.GET.get('review', None)
	rating = request.GET.get('rating', 0)

	# Check if feedback is cached, if not, cache it
	fbc = cache.get('feedback')
	if fbc is None:
		# If feedback is not cached, create a new feedback object with csv files and cache it
		fbc = feedback('static/business_feedback.csv','static/rest_review_feedback.csv')
		cache.set('feedback', fbc)

	# Add the review and rating to the feedback object
	fbc.add_to_df(userId,businessId, date.today(),rating, review)

	# Create a status dictionary with status code 200
	status = {
		"status": 200
	}

	# Return the status dictionary as a JsonResponse
	return JsonResponse(status)


business = None
hybridRS = None
def exploreTheBeyondRecommendations(request):
	# Check if the cached business data is available
	business = cache.get('business')
	if business is None:
		# If not, read the business data from a CSV file
		business = pd.read_csv('static/business_content.csv')
		# Cache the business data for future use
		cache.set('business', business)

	# Create an instance of the content-based recommender system
	rec = ContentBasedRS(business)

	# Get the query from the GET parameters in the request
	query = request.GET.get('query', None)

	# Get the recommendations based on the query
	output_data = rec.recommend(query)

	# Filter the output data and convert it to a list of dictionaries
	filtered_data = output_data[['name', 'latitude', 'longitude', 'categories','scores', 'business_id']].to_dict(orient='records')

	# Create a list of restaurants based on the filtered data
	restaurants = []
	for restaurant in filtered_data:
		restaurants.append({
			'name': restaurant['name'],
			'latitude': restaurant['latitude'],
			'longitude': restaurant['longitude'],
			'tags': restaurant['categories'],
			'scores':restaurant['scores'],
			'business_id': restaurant['business_id']
		})

	# Create a dictionary containing the list of restaurants
	data = {
		"restaurants": restaurants
	}

	# Return the response as a JSON object
	return JsonResponse(data)

def bestNearbyRecommendations(request):
	# Get the user ID, latitude, and longitude from the request object
	userId = request.GET.get('userId', None)
	lat = request.GET.get('lat', None)
	long = request.GET.get('long', None)

	# Get the business and restaurant review data from the cache, if available
	business_loc = cache.get('business_loc')
	rest_review = cache.get('rest_review')
	rec_loc = cache.get('rec_loc')

	# If the business location data is not in the cache, load it from the CSV file and add it to the cache
	if (business_loc is None):
		business_loc = pd.read_csv('static/business_content.csv')
		cache.set('business_loc', business_loc)

	# If the restaurant review data is not in the cache, load it from the CSV file and add it to the cache
	if (rest_review is None):
		rest_review = pd.read_csv('static/rest_review_content.csv')
		cache.set('rest_review', rest_review)

	# If the content-based location recommender is not in the cache, create it and add it to the cache
	if (rec_loc is None):
		rec_loc = ContentBased_locRS(rest_review, business_loc)
		cache.set('rec_loc', rec_loc)

	# Use the recommender to get the recommended restaurants
	output, recc = rec_loc.fit(userId, lat, long)
	restaurants = []
	for i, row in recc.iterrows():
		# Add the restaurant information to the list of recommended restaurants
		restaurants.append({
			'name': row['name'].strip(),
			'latitude': row['latitude'],
			'longitude': row['longitude'],
			'distance': row['distance'],
			'tags': row['categories'],
			'scores': row['scores'],
			'business_id': row['business_id']
		})

	# Create a dictionary containing the recommended restaurants and return it as a JSON response
	data = {
		"restaurants": restaurants
	}

	return JsonResponse(data)

def topPlacesRecommendations(request):
	# Get the parameters from the request
	lat = request.GET.get('lat', None)
	long = request.GET.get('long', None)
	cuisines = request.GET.get('cuisines', None)
	userId = request.GET.get('userId', None)

	# Check if business and review dataframes are cached, if not, read them from file and cache them
	businessDF = cache.get('businessDF')
	restReviewDF = cache.get('restReviewDF')
	if businessDF is None:
		businessDF = pd.read_csv('static/business_content.csv')
		cache.set('businessDF', businessDF)

	if restReviewDF is None:
		restReviewDF = pd.read_csv('static/rest_review_content.csv')
		cache.set('restReviewDF', restReviewDF)

	# Get restaurant recommendations based on user preferences
	recommendations = get_recommendations(userId, restReviewDF, businessDF, lat, long, cuisines)

	restaurants = []
	for i, restaurant in recommendations.iterrows():
		# Add restaurant data to the response JSON object
		restaurants.append({
			'name': restaurant['name'],
			'latitude': restaurant['latitude'],
			'longitude': restaurant['longitude'],
			'distance': restaurant['distance'],
			'tags':restaurant['categories'],
			'scores': 100,
			'business_id':restaurant['business_id']
		})

	data = {
		"restaurants": restaurants
	}

	# Return the response as a JSON object
	return JsonResponse(data)

def feelingLuckyRecommendations(request):
	userId = request.GET.get('userId', None)
	hybridRS = cache.get('hybridRS')
	if hybridRS is None:
		# If the recommendation model has not been cached, load the business and review data,
		# train the hybrid recommendation system, and cache it for future use.
		hybridRS = Hybrid_rec('static/business2.csv', 'static/rest_review2.csv')
		cache.set('hybridRS', hybridRS)

	# Get recommendations for the specified user from the cached hybrid recommendation system.
	filtered_data = hybridRS.recommend(userId, 10)

	# Format the recommendation data as a list of dictionaries.
	restaurants = []
	for i, restaurant in filtered_data.iterrows():
		restaurants.append({
			'name': restaurant['name'],
			'latitude': restaurant['latitude'],
			'longitude': restaurant['longitude'],
			'tags': restaurant['categories'],
			'scores': restaurant['scores'],
			'business_id': restaurant['business_id']
		})

	# Format the recommendation data as a dictionary and return it as a JSON response.
	data = {
		"restaurants": restaurants
	}

	return JsonResponse(data)


