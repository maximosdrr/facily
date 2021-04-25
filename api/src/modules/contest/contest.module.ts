import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Contest } from 'src/entities/contest.entity';
import { Todo } from 'src/entities/todo.entity';
import { Winners } from 'src/entities/winners.entity';
import { ContestController } from './contest.controller';
import { ContestService } from './contest.service';

@Module({
  controllers: [ContestController],
  providers: [ContestService],
  imports: [TypeOrmModule.forFeature([Contest, Winners, Todo])],
})
export class ContestModule {}
