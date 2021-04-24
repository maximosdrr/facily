import { Column, Entity, ManyToOne, PrimaryGeneratedColumn } from 'typeorm';
import { Contest } from './contest.entity';

@Entity()
export class Winners {
  @PrimaryGeneratedColumn('uuid')
  id?: string;

  @Column()
  amount: number;

  @Column({ type: 'double precision' })
  award: number;

  @Column()
  description: string;

  @Column()
  range: number;

  @ManyToOne(() => Contest, (contest) => contest.winners, {
    onDelete: 'CASCADE',
    nullable: false,
  })
  contest: Contest;
}
