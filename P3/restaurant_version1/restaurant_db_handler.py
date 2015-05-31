from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurant_version1.database_setup import Base, Restaurant


class RestaurantDBHandler(object):

    def __init__(self):
        pass

    def create_session(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine
        db_session = sessionmaker(bind=engine)

        session = db_session()
        return session

    def list_restaurants(self):
        session = self.create_session()

        __list = session.query(Restaurant).all()

        restaurant_name = []

        for item in __list:
            print item.name
            restaurant_name.append(item.name)

        print "List of Restaurants:\n" + str(restaurant_name)
        return restaurant_name

    def lookup_restaurant(self, lookup_name):
        session = self.create_session()
        returned_data = session.query(Restaurant).filter_by(name=lookup_name)

        restaurant_name = []

        for item in returned_data:
            print "Name: " + str(item.name)
            print "ID: " + str(item.id)
            restaurant_name.append((item.name, item.id),)

        return restaurant_name

    def add_restaurant(self, new_restaurant):
        session = self.create_session()

        rest_to_add = Restaurant(name=new_restaurant)
        session.add(rest_to_add)
        session.commit()

    def delete_restaurants_by_name(self, delete_restaurant):
        session = self.create_session()

        rest_to_delete = session.query(Restaurant).filter_by(name=delete_restaurant)

        for item in rest_to_delete:
            session.delete(item)
            session.commit()
            print "Restaurant: " + str(item.name) + " id: " + str(item.id) + " deleted"
#
#     def AddRestaurant(self, NewRestaurantName):
#         session = self.createSession()
#         RestaurantToAdd = Restaurant(name=NewRestaurantName)
#         session.add(RestaurantToAdd)
#         session.commit()
#
#         try:
#             result = self.LookUpRestaurant(NewRestaurantName)
#             return result
#         except:
#             msg = "Error: Can not verify Restaurant Added"
#             print(msg)
#             return msg

#     def RenameRestaurant(self, NameToChange, ChangeNameTo):
#         session = self.createSession()
#
#         RestaurantToUpdate = session.query(Restaurant).filter_by(name = NameToChange)
#         RestaurantToUpdate.name = ChangeNameTo
#         session.add(RestaurantToUpdate)
#         session.execute()
#         session.commit()
#
#         results = session.query(Restaurant).filter_by(name = ChangeNameTo)
#         return results
