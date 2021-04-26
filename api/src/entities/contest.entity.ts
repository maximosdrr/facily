import { Column, Entity, OneToMany, PrimaryGeneratedColumn } from 'typeorm';
import { Winners } from './winners.entity';
import { ContestTypes } from '../models/contest-types';
@Entity()
export class Contest {
  @PrimaryGeneratedColumn('uuid')
  id?: string;

  @Column({ type: 'enum', enum: ContestTypes, default: ContestTypes.UNTYPE })
  type: string;

  @Column('int', { array: true })
  result: number[] | string[];

  @Column()
  location: string;

  @Column()
  index: number;

  @Column({ type: 'double precision' })
  accumulatedSpecialValue: number;

  @Column({ type: 'double precision' })
  accumulatedValue: number;

  @Column({ type: 'double precision' })
  accumulatedValueForNextContest: number;

  @Column({ type: 'double precision' })
  collected: number;

  @Column({ type: 'double precision' })
  estimatedValueForNextContest: number;

  @OneToMany(() => Winners, (winners) => winners.contest)
  winners: Winners[];
}
