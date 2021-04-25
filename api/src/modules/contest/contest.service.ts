import {
  BadRequestException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Contest } from 'src/entities/contest.entity';
import { Todo } from 'src/entities/todo.entity';
import { Winners } from 'src/entities/winners.entity';
import { Repository } from 'typeorm';

@Injectable()
export class ContestService {
  constructor(
    @InjectRepository(Contest)
    private readonly contestRepo: Repository<Contest>,

    @InjectRepository(Winners)
    private readonly winnersRepo: Repository<Winners>,

    @InjectRepository(Todo)
    private readonly todoRepo: Repository<Todo>,
  ) {}

  saveContest(contest: Contest) {
    try {
      return this.contestRepo.save(contest);
    } catch (e) {
      console.log(e);
      throw new BadRequestException('Algo deu errado');
    }
  }

  async saveWinners(winners: Winners[]) {
    for (let i = 0; i < winners.length; i++) {
      try {
        await this.winnersRepo.save(winners[i]);
      } catch (e) {
        console.log(e);
        throw new BadRequestException('Something is wrong');
      }
    }

    return winners;
  }

  saveTodo(todo: Todo) {
    try {
      return this.todoRepo.save(todo);
    } catch (e) {
      console.log(e);
      throw new BadRequestException('Something is wrong');
    }
  }

  findAllTodos() {
    try {
      return this.todoRepo.find();
    } catch (e) {
      console.log(e);
      throw new BadRequestException('Something is wrong');
    }
  }

  findAllContests() {
    try {
      return this.contestRepo.find({
        join: {
          alias: 'contest',
          leftJoinAndSelect: {
            winners: 'contest.winners',
          },
        },
      });
    } catch (e) {
      console.log(e);
      throw new BadRequestException('Something is wrong');
    }
  }

  findOneContest(id: string) {
    try {
      return this.contestRepo.findOne(id, {
        join: {
          alias: 'contest',
          leftJoinAndSelect: {
            winners: 'contest.winners',
          },
        },
      });
    } catch (e) {
      throw new BadRequestException('Something is wrong');
    }
  }

  async deleteContest(id: string) {
    try {
      const contestToDelete = await this.contestRepo.findOne(id);
      if (!contestToDelete)
        throw new NotFoundException('This contest not exists');

      return this.contestRepo.delete(id);
    } catch (e) {
      throw new BadRequestException('Something is wrong');
    }
  }
}
