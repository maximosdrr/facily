import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Contest } from './entities/contest.entity';
import { Winners } from './entities/winners.entity';
import { ContestModule } from './modules/contest/contest.module';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: 'localhost',
      port: 5432,
      username: 'admin',
      password: 'admin',
      database: 'facily',
      entities: [Contest, Winners],
      synchronize: true,
    }),
    ContestModule,
  ],
  controllers: [AppController],
  providers: [],
})
export class AppModule {}
