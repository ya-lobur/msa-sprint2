import {ApolloServer} from '@apollo/server';
import {startStandaloneServer} from '@apollo/server/standalone';
import {buildSubgraphSchema} from '@apollo/subgraph';
import gql from 'graphql-tag';
import fetch from 'node-fetch';

const HOTEL_SERVICE_URL = process.env.HOTEL_SERVICE_URL || 'http://hotelio-monolith:8080';

const typeDefs = gql`
    type Hotel @key(fields: "id") {
        id: ID!
        city: String
        rating: Float
        description: String
        operational: Boolean
        fullyBooked: Boolean
    }

    type Query {
        hotelsByIds(ids: [ID!]!): [Hotel]
    }
`;

async function fetchHotel(id) {
    try {
        const response = await fetch(`${HOTEL_SERVICE_URL}/api/hotels/${id}`);
        if (!response.ok) {
            console.error(`Failed to fetch hotel ${id}: ${response.status}`);
            return null;
        }
        const data = await response.json();
        console.log(`✅ Retrieved hotel ${id} in ${data.city}`);
        return {
            id: data.id,
            city: data.city,
            rating: data.rating,
            description: data.description,
            operational: data.operational,
            fullyBooked: data.fullyBooked
        };
    } catch (error) {
        console.error(`Error fetching hotel ${id}:`, error);
        return null;
    }
}

const resolvers = {
    Hotel: {
        __resolveReference: async ({id}) => {
            console.log(`Resolving Hotel reference for id: ${id}`);
            return await fetchHotel(id);
        },
    },
    Query: {
        hotelsByIds: async (_, {ids}) => {
            console.log(`Fetching hotels by ids: ${ids}`);
            const hotels = await Promise.all(ids.map(id => fetchHotel(id)));
            return hotels.filter(hotel => hotel !== null);
        },
    },
};

const server = new ApolloServer({
    schema: buildSubgraphSchema([{typeDefs, resolvers}]),
});

startStandaloneServer(server, {
    listen: {port: 4002},
}).then(() => {
    console.log('✅ Hotel subgraph ready at http://localhost:4002/');
});
