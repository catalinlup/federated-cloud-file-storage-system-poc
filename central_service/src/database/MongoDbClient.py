from typing import List, Tuple
from pymongo import MongoClient



class MongoDbClient:
    """
    Implements the database interactions for the MongoDB database.
    """

    def __init__(self, connection_string: str, database_name: str='doc-heart') -> None:
        """Initializes a MongoDb client.

        Keyword arguments:
        connection_string -- the string used to connect to the mongo DB database.
        database_name -- the name of the database to connect to (default: doc-heart)
        """
        super().__init__()
        self.connection_string = connection_string
        self.client = MongoClient(connection_string)
        self.db_ref = self.client[database_name]

    def save(self, entity_name: str, entity_content: dict, collection_name: str) -> bool:
        """Saves the provided JSON entity (of the given entity_name and entity_content) into a collection of the provided collection_name.
           Returns true if the entity was saved succesfully, false otherwise.

        Keyword arguments:
        entity_name -- the name of the JSON entity to be saved.
        entity_content -- the content of the JSON entity to be saved.
        collection_name -- the collection in which the JSON entity will be saved.
        """
        
        collection_ref = self.db_ref[collection_name]

        # check if id already exists. If it is the case, overwrite
        if collection_ref.count_documents({'_id': entity_name}) > 0:
            collection_ref.delete_many({'_id': entity_name})

        entity_content['_id'] = entity_name
        saved_instance = collection_ref.insert_one(entity_content)

        return (saved_instance is not None)

    
    def get_by_name(self, entity_name: str, collection_name: str) -> dict:
        """Retrieves an entity from the the database by its name. Returns the contents of the entity.

        Keyword arguments:
        entity_name -- the name of the JSON entity to be retrieved.
        collection_name -- the name of the collection to retrieve the JSON entity from. 
        """

        collection_ref = self.db_ref[collection_name]
        retrieved_entity = collection_ref.find_one(entity_name)
        return retrieved_entity

    
    def get_all_by_attribute(self, attribute_name: str, attribute_value: str, collection_name: str) -> List[dict]:
        """
        Retrieves a list of all entitites that have as the attribute name the specified attribute value.

        Keyword arguments:
        attribute_name -- the name of the attribute to query by
        attribute_value -- the target attribute value we are looking for
        collection_name -- the name of the collection to query from
        """

        collection_ref = self.db_ref[collection_name]
        retrieved_entities = collection_ref.find({attribute_name: attribute_value})
        return retrieved_entities
    

    def get_all_by_attributes(self, attribute_name_value_pairs: List[Tuple[str, str]], collection_name: str) -> List[dict]:
        """
        Retrieves the list of all entities that have as attributes the specified attribute values.

        Keyword arguments:
        attribute_name_value_pairs -- list specifying the expected value for each attribute.
        collection_name -- the name of the collection to query from
        """

        collection_ref = self.db_ref[collection_name]
        query_dict = dict()
        
        for attribute_name, attribute_value in attribute_name_value_pairs:
            query_dict[attribute_name] = attribute_value
        
        retrieved_entities = collection_ref.find(query_dict)
        return retrieved_entities



        
    

    def get_all(self, collection_name: str) -> List[Tuple[str, dict]]:
        """Retrieves all entities from the collection. Returns a list of tuples containing the names and contents of each entity.

        Keyword arguments:
        collection_name -- the name of the collection to retrieve the entites from.
        """
        collection_ref = self.db_ref[collection_name]
        retrieved_entities = collection_ref.find()
        entity_list = [(entity['_id'], entity) for entity in retrieved_entities]
        return entity_list


    def get_all_by_query(self, query: dict, collection_name: str) -> List[dict]:
        """Retrieves all the entities based on the provided query.

        Keyword arguments:
        collection_name -- the name of the collection to retrieve entities from
        query -- the dictionary encoding the query
        """

        collection_ref = self.db_ref[collection_name]
        retrieved_entities = collection_ref.find(query)
        return list(retrieved_entities)


    def perform_aggregation(self, aggregation_pipeline: List[dict], collection_name: str) -> dict:
        """
        Performs an aggregation operation on the following 
        Keyword arguments:
        aggegation_pipeline -- the aggregation pipeline to be used for the queries.
        collection_name -- the name of the collection to retrieve the entities from.
        """

        collection_ref = self.db_ref[collection_name]
        aggregation_result = collection_ref.aggregate(aggregation_pipeline)
        return list(aggregation_result)
    



    def remove_all_by_id(self, ids: List[str], collection_name: str) -> int:
        """
        Removes all the documents by their ids.

        Keyword arguments:
        ids -- the list of ids of the documents to be removed
        collection_name -- the name of the collection to remove from
        """

        collection_ref = self.db_ref[collection_name]
        res = collection_ref.delete_many({'_id':{'$in': ids}})

        return res.deleted_count
