import {ApolloServer} from '@apollo/server';
import {startStandaloneServer} from '@apollo/server/standalone';
import {buildSubgraphSchema} from '@apollo/subgraph';
import gql from 'graphql-tag';
import grpc from '@grpc/grpc-js';
import protoLoader from '@grpc/proto-loader';
import {fileURLToPath} from 'url';
import {dirname, join} from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const PROTO_PATH = join(__dirname, 'booking.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
});

const bookingProto = grpc.loadPackageDefinition(packageDefinition).booking;
const GRPC_HOST = process.env.BOOKING_SERVICE_HOST || 'booking-service';
const GRPC_PORT = process.env.BOOKING_SERVICE_PORT || '50051';

const grpcClient = new bookingProto.BookingService(
    `${GRPC_HOST}:${GRPC_PORT}`,
    grpc.credentials.createInsecure()
);

const typeDefs = gql`
    type Booking @key(fields: "id") {
        id: ID!
        userId: String!
        hotelId: String!
        promoCode: String
        discountPercent: Float
        hotel: Hotel
    }

    extend type Hotel @key(fields: "id") {
        id: ID! @external
    }

    type Query {
        bookingsByUser(userId: String!): [Booking]
    }

`;

const resolvers = {
    Query: {
        bookingsByUser: async (_, {userId}, {req}) => {
            // ACL: Check if user is authorized
            const requestUserId = req.headers['userid'];

            if (!requestUserId) {
                console.log('❌ No userid header provided');
                return [];
            }

            if (requestUserId !== userId) {
                console.log(`❌ ACL denied: user ${requestUserId} tried to access bookings of ${userId}`);
                return [];
            }

            console.log(`✅ ACL passed: user ${requestUserId} accessing own bookings`);

            // Call gRPC service
            return new Promise((resolve, reject) => {
                grpcClient.ListBookings({user_id: userId}, (error, response) => {
                    if (error) {
                        console.error('gRPC error:', error);
                        reject(error);
                        return;
                    }

                    const bookings = response.bookings.map(b => ({
                        id: b.id,
                        userId: b.user_id,
                        hotelId: b.hotel_id,
                        promoCode: b.promo_code,
                        discountPercent: b.discount_percent
                    }));

                    console.log(`✅ Retrieved ${bookings.length} bookings for user ${userId}`);
                    resolve(bookings);
                });
            });
        },
    },
    Booking: {
        hotel: (booking) => {
            return {__typename: 'Hotel', id: booking.hotelId};
        },
    },
};

const server = new ApolloServer({
    schema: buildSubgraphSchema([{typeDefs, resolvers}]),
});

startStandaloneServer(server, {
    listen: {port: 4001},
    context: async ({req}) => ({req}),
}).then(() => {
    console.log('✅ Booking subgraph ready at http://localhost:4001/');
});
